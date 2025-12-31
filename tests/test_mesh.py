import json
import pytest
from core.gear_factory import GearFactory
from gears.spur import SpurGear


def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)


def test_mesh_spur_gears():
    """Test 16: Analyse d'engrènement entre deux engrenages droits (gear1.json, gear2.json)"""
    # Enregistrer le type 'spur' dans la factory pour ce test
    GearFactory.register_gear('spur', SpurGear)

    config1 = load_config('gear1.json')
    config2 = load_config('gear2.json')

    gear1 = GearFactory.from_dict(config1)
    gear2 = GearFactory.from_dict(config2)

    center_distance, contact_ratio = gear1.mesh_with(gear2)

    # Vérifications basées sur les fichiers de configuration fournis
    assert pytest.approx(center_distance, rel=1e-3) == 60.0
    assert pytest.approx(contact_ratio, rel=1e-2) == 1.64
