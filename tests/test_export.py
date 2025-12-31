import os
import struct
from core.base_gear import GearParams
from core.gear_factory import GearFactory
from gears.spur import SpurGear
from export.step import STEPExporter
from export.stl import STLExporter


def test_export_step_file(tmp_path):
    # Register spur gear
    GearFactory.register_gear('spur', SpurGear)

    params = GearParams(name='ExportStep', module=2.0, teeth=24, pressure_angle=20.0, face_width=12.0)
    gear = GearFactory.create_gear('spur', params)

    out = tmp_path / 'export_test.step'
    exporter = STEPExporter()
    exporter.export_gear(gear, str(out))

    assert out.exists(), "STEP file was not created"

    text = out.read_text()
    assert 'ISO-10303-21' in text
    # Check that a CIRCLE entity (primitive) exists
    assert 'CIRCLE' in text
    # Check that the radius value (pitch_diameter/2) appears
    expected_radius = gear.pitch_diameter / 2
    assert str(expected_radius) in text


def test_export_stl_file(tmp_path):
    # Register spur gear
    GearFactory.register_gear('spur', SpurGear)

    params = GearParams(name='ExportSTL', module=2.0, teeth=24, pressure_angle=20.0, face_width=8.0)
    gear = GearFactory.create_gear('spur', params)

    out = tmp_path / 'export_test.stl'
    STLExporter.export_gear(gear, str(out), resolution=32)

    assert out.exists(), "STL file was not created"
    # File should be binary and have at least header + some faces
    size = out.stat().st_size
    assert size > 100, "STL file seems too small"

    # Check header begins with expected text
    with open(out, 'rb') as f:
        header = f.read(23)
    assert header.startswith(b'Binary STL - Gear Model')
