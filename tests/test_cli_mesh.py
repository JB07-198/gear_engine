import json
import subprocess
import sys


def test_cli_mesh_outputs(tmp_path):
    gear1 = tmp_path / "gear1.json"
    gear2 = tmp_path / "gear2.json"

    gear1.write_text(json.dumps({
        "name": "gear1",
        "type": "spur",
        "module": 2.0,
        "teeth": 20,
        "face_width": 10.0,
        "pressure_angle": 20.0,
    }))

    gear2.write_text(json.dumps({
        "name": "gear2",
        "type": "spur",
        "module": 2.0,
        "teeth": 40,
        "face_width": 10.0,
        "pressure_angle": 20.0,
    }))

    cmd = [sys.executable, "main.py", "mesh", "--gear1", str(gear1), "--gear2", str(gear2)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout

    assert "Engrenage 1" in out
    assert "Engrenage 2" in out
    assert "Distance entre centres" in out
    assert "Rapport de contact" in out
    assert "✓ Rapport de contact bon" in out or "Rapport de contact bon" in out
