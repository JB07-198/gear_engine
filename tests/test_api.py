import json
from pathlib import Path


def test_api_endpoints(tmp_path):
    from interfaces.api import app

    client = app.test_client()

    # Health
    r = client.get('/api/health')
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('status') == 'healthy'

    # Types
    r = client.get('/api/gear/types')
    assert r.status_code == 200
    data = r.get_json()
    assert 'types' in data and 'spur' in data['types']

    # Create gear
    gear_params = {
        'name': 'api_spur',
        'module': 2.0,
        'teeth': 20,
        'pressure_angle': 20.0,
        'face_width': 10.0,
    }

    r = client.post('/api/gear/create', json={'type': 'spur', 'params': gear_params})
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('success') is True
    assert 'gear' in data

    # Analyze gear
    r = client.post('/api/gear/analyze', json={'gear': {'type': 'spur', 'params': gear_params}})
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('success') is True
    assert 'analysis' in data

    # Mesh two gears
    gear1 = {'type': 'spur', 'params': gear_params}
    gear2 = {'type': 'spur', 'params': {**gear_params, 'name': 'api_spur_2', 'teeth': 40}}

    r = client.post('/api/gear/mesh', json={'gear1': gear1, 'gear2': gear2})
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('success') is True
    assert 'mesh_analysis' in data
    ma = data['mesh_analysis']
    assert 'center_distance' in ma and 'contact_ratio' in ma

    # Export STEP
    filename = tmp_path / 'api_gear.step'
    r = client.post('/api/export/step', json={'gear': gear1, 'filename': str(filename)})
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('success') is True
    assert filename.exists()
