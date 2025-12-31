from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse
from typing import Dict, Any
import uuid
import os

from core.gear_factory import GearFactory
from core.base_gear import GearParams
from core import export_db
from core import auth
from interfaces import task_runner

REQUIRE_AUTH = os.environ.get('REQUIRE_AUTH', 'false').lower() == 'true'

export_db.init_db()

app = FastAPI(title="Gear Engine API (FastAPI)")


@app.get('/health')
def health():
    return {'status': 'healthy', 'service': 'gear_engine_fastapi'}


@app.post('/auth/register')
def register(payload: Dict[str, Any]):
    try:
        username = payload.get('username')
        password = payload.get('password')
        if not username or not password:
            raise ValueError('username and password required')
        token = auth.register_user(username, password)
        return {'success': True, 'token': token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/auth/login')
def login(payload: Dict[str, Any]):
    try:
        username = payload.get('username')
        password = payload.get('password')
        if not username or not password:
            raise ValueError('username and password required')
        token = auth.authenticate_user(username, password)
        if not token:
            raise HTTPException(status_code=401, detail='Invalid credentials')
        return {'success': True, 'token': token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/gear/types')
def get_gear_types():
    types = GearFactory.get_available_types()
    return {'types': types, 'count': len(types)}


@app.post('/gear/create')
def create_gear(payload: Dict[str, Any]):
    try:
        gear_type = payload.get('type', 'spur')
        params_dict = payload.get('params', payload)
        params = GearParams(**params_dict)
        gear = GearFactory.create_gear(gear_type, params)
        return {'success': True, 'gear': gear.get_info()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/gear/analyze')
def analyze_gear(payload: Dict[str, Any]):
    try:
        if 'gear' not in payload:
            raise ValueError('Configuration d\'engrenage requise')
        gear = GearFactory.from_dict(payload['gear'])
        info = gear.get_info()
        analysis = {
            'basic_info': info,
            'performances': {'bending_stress': 'N/A', 'contact_stress': 'N/A'},
            'validations': []
        }
        return {'success': True, 'analysis': analysis}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/gear/mesh')
def mesh_gears(payload: Dict[str, Any]):
    try:
        if 'gear1' not in payload or 'gear2' not in payload:
            raise ValueError('Deux engrenages requis')
        gear1 = GearFactory.from_dict(payload['gear1'])
        gear2 = GearFactory.from_dict(payload['gear2'])
        center_distance, contact_ratio = gear1.mesh_with(gear2)
        transmission_ratio = gear2.params.teeth / gear1.params.teeth
        return {
            'success': True,
            'mesh_analysis': {
                'center_distance': center_distance,
                'contact_ratio': contact_ratio,
                'transmission_ratio': transmission_ratio,
                'gear1_info': gear1.get_info(),
                'gear2_info': gear2.get_info()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def _do_export(format: str, gear_dict: Dict[str, Any], filename: str, job_id: str):
    try:
        gear = GearFactory.from_dict(gear_dict)
        if format.lower() == 'step':
            from export.step import STEPExporter
            exporter = STEPExporter()
            exporter.export_gear(gear, filename)
        elif format.lower() == 'stl':
            from export.stl import STLExporter
            exporter = STLExporter()
            exporter.export_gear(gear, filename)
        else:
            raise ValueError('Format non supporté')
        export_db.update_job_status(job_id, 'done', None)
    except Exception as e:
        export_db.update_job_status(job_id, 'error', str(e))


@app.post('/export')
def export_gear(payload: Dict[str, Any], background_tasks: BackgroundTasks, request: Request):
    try:
        fmt = payload.get('format', 'step')
        gear = payload.get('gear')
        filename = payload.get('filename') or f"gear_{uuid.uuid4().hex}.{fmt}"
        # ensure directory exists
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        job_id = uuid.uuid4().hex
        # Authentication handling
        if REQUIRE_AUTH:
            # expect Authorization: Bearer <jwt>
            auth_header = request.headers.get('authorization')
            if not auth_header or not auth_header.lower().startswith('bearer '):
                raise HTTPException(status_code=401, detail='Authorization required')
            jwt_token = auth_header.split(None, 1)[1]
            username = auth.verify_token(jwt_token)
            if not username:
                raise HTTPException(status_code=401, detail='Invalid token')
            export_db.add_job(job_id, filename, fmt, None, username)
            # submit task
            task_runner.submit_task(_do_export, fmt, gear, filename, job_id)
            return {'success': True, 'job_id': job_id, 'filename': filename}
        else:
            # legacy mode: return a download token
            client_token = payload.get('token')
            token = client_token or uuid.uuid4().hex
            export_db.add_job(job_id, filename, fmt, token, None)
            task_runner.submit_task(_do_export, fmt, gear, filename, job_id)
            return {'success': True, 'job_id': job_id, 'filename': filename, 'token': token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/export/{job_id}')
def export_status(job_id: str):
    job = export_db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')
    return job


@app.get('/jobs')
def list_my_jobs(request: Request):
    if REQUIRE_AUTH:
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.lower().startswith('bearer '):
            raise HTTPException(status_code=401, detail='Authorization required')
        jwt_token = auth_header.split(None, 1)[1]
        username = auth.verify_token(jwt_token)
        if not username:
            raise HTTPException(status_code=401, detail='Invalid token')
        jobs = export_db.list_jobs(username)
        return {'success': True, 'jobs': jobs}
    else:
        jobs = export_db.list_jobs()
        return {'success': True, 'jobs': jobs}


@app.post('/jobs/{job_id}/revoke')
def revoke_job(job_id: str, request: Request, payload: Dict[str, Any] = None):
    # When auth required, validate ownership via JWT; otherwise require token in payload
    job = export_db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')
    if REQUIRE_AUTH:
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.lower().startswith('bearer '):
            raise HTTPException(status_code=401, detail='Authorization required')
        jwt_token = auth_header.split(None, 1)[1]
        username = auth.verify_token(jwt_token)
        if not username:
            raise HTTPException(status_code=401, detail='Invalid token')
        if job.get('username') != username:
            raise HTTPException(status_code=403, detail='Not allowed to revoke this job')
        ok = export_db.revoke_job(job_id)
        return {'success': ok}
    else:
        data = payload or {}
        token = data.get('token')
        if job.get('token') != token:
            raise HTTPException(status_code=403, detail='Invalid token')
        ok = export_db.revoke_job(job_id)
        return {'success': ok}


@app.get('/download')
def download_file(job_id: str, token: str = None, request: Request = None):
    job = export_db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')
    # If auth required, validate JWT from Authorization header and ensure job owner matches
    if REQUIRE_AUTH:
        auth_header = request.headers.get('authorization') if request else None
        if not auth_header or not auth_header.lower().startswith('bearer '):
            raise HTTPException(status_code=401, detail='Authorization required')
        jwt_token = auth_header.split(None, 1)[1]
        username = auth.verify_token(jwt_token)
        if not username:
            raise HTTPException(status_code=403, detail='Invalid token')
        if job.get('username') != username:
            raise HTTPException(status_code=403, detail='Not allowed to download this job')
    else:
        # legacy download token
        if job.get('token') != token:
            raise HTTPException(status_code=403, detail='Invalid token')
    path = job.get('filename')
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail='File not found')
    return FileResponse(path, filename=os.path.basename(path))


def run(host: str = '0.0.0.0', port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)
