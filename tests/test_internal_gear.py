import pytest
import math
from core.base_gear import GearParams
from core.gear_factory import GearFactory
from gears.internal import InternalGear
from gears.spur import SpurGear

class TestInternalGear:
    def test_internal_creation(self):
        params = GearParams(name='Internal1', module=2.0, teeth=60, pressure_angle=20.0, face_width=10.0)
        gear = InternalGear(params)
        assert gear is not None
        info = gear.get_info()
        assert info['type'] == 'InternalGear'
        assert info['gear_type'] == 'internal'

    def test_internal_properties(self):
        params = GearParams(name='Internal2', module=2.0, teeth=60, pressure_angle=20.0, face_width=10.0)
        gear = InternalGear(params)
        # pitch diameter = module * teeth
        assert gear.pitch_diameter == pytest.approx(2.0 * 60)
        # outside and root diameters according to InternalGear definitions
        assert gear.outside_diameter == pytest.approx(gear.pitch_diameter - 2 * params.module)
        assert gear.root_diameter == pytest.approx(gear.pitch_diameter + 2 * 1.25 * params.module)
        assert gear.addendum == pytest.approx(2.0)
        assert gear.dedendum == pytest.approx(1.25 * 2.0)

    def test_internal_mesh_with_spur(self):
        # register types
        GearFactory.register_gear('internal', InternalGear)
        GearFactory.register_gear('spur', SpurGear)

        internal_params = GearParams(name='Internal3', module=2.0, teeth=60, pressure_angle=20.0, face_width=10.0)
        spur_params = GearParams(name='Pinion', module=2.0, teeth=20, pressure_angle=20.0, face_width=10.0)

        internal = InternalGear(internal_params)
        spur = SpurGear(spur_params)

        center_distance, contact_ratio = internal.mesh_with(spur)
        assert center_distance == pytest.approx((internal.pitch_diameter - spur.pitch_diameter) / 2)
        assert contact_ratio >= 0
