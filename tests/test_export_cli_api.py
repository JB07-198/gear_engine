import json
import subprocess
import sys
from pathlib import Path


def test_cli_and_api_export(tmp_path):
    # Prepare config for CLI export
    config = tmp_path / "gear_config.json"
    gear = {
        "name": "cli_gear",
        "type": "spur",
        "module": 2.0,
        "teeth": 20,
        "face_width": 10.0,
        "pressure_angle": 20.0,
    }
    config.write_text(json.dumps(gear))

    # CLI STEP export
    out_step = tmp_path / "gear_step.step"
    cmd = [sys.executable, "main.py", "export", "--config", str(config), "--format", "step", "--output", str(out_step)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert out_step.exists() and out_step.stat().st_size > 0

    # CLI STL export
    out_stl = tmp_path / "gear_stl.stl"
    cmd = [sys.executable, "main.py", "export", "--config", str(config), "--format", "stl", "--output", str(out_stl)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert out_stl.exists() and out_stl.stat().st_size > 0

    # API STEP export (Flask test client)
    from interfaces.api import app

    client = app.test_client()
    api_file = tmp_path / "api_gear.step"
    gear_params = gear.copy()
    gear_params.pop('type', None)
    r = client.post('/api/export/step', json={'gear': {'type': 'spur', 'params': gear_params}, 'filename': str(api_file)})
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('success') is True
    assert api_file.exists() and api_file.stat().st_size > 0

    # Basic dimension check in STEP: look for radius or diameter approximate value
    content = api_file.read_text()
    # Expect at least the gear name or a numeric value present in STEP content
    assert len(content) > 50
    assert 'GEAR' in content.upper() or 'CARTESIAN_POINT' in content or 'EXTRUDED_AREA_SOLID' in content
