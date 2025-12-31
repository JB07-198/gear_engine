import pytest
import math
from core.base_gear import GearParams
from gears.rack import RackGear
from gears.spur import SpurGear

class TestRackGear:
    def test_rack_creation(self):
        params = GearParams(name='Rack1', module=2.0, teeth=20, pressure_angle=20.0, face_width=10.0)
        rack = RackGear(params)
        assert rack is not None
        assert rack.get_info()['gear_type'] == 'rack'

    def test_rack_properties(self):
        params = GearParams(name='Rack2', module=2.0, teeth=20, pressure_angle=20.0, face_width=10.0)
        rack = RackGear(params)
        assert math.isinf(rack.pitch_diameter)
        assert rack.tooth_height == pytest.approx(2.25 * params.module)
        assert rack.tooth_thickness == pytest.approx(math.pi * params.module / 2)

    def test_rack_tooth_profile(self):
        params = GearParams(name='Rack3', module=2.0, teeth=20, pressure_angle=20.0, face_width=10.0)
        rack = RackGear(params)
        profile = rack.get_tooth_profile()
        assert isinstance(profile, list)
        assert len(profile) >= 4

    def test_rack_mesh_with_spur(self):
        rack_params = GearParams(name='Rack4', module=2.0, teeth=20, pressure_angle=20.0, face_width=10.0)
        rack = RackGear(rack_params)
        spur_params = GearParams(name='SpurRack', module=2.0, teeth=40, pressure_angle=20.0, face_width=10.0)
        spur = SpurGear(spur_params)

        center_distance, contact_ratio = rack.mesh_with(spur)
        assert center_distance == pytest.approx(spur.pitch_diameter / 2)
        assert contact_ratio > 0
