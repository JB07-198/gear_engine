"""
Tests pour la classe GearFactory
"""
import unittest
from core.gear_factory import GearFactory
from core.base_gear import GearParams
from gears.spur import SpurGear
from gears.helical import HelicalGear
from gears.bevel import BevelGear
from gears.worm import WormGear
from gears.rack import RackGear
from gears.internal import InternalGear


class TestGearFactoryRegistration(unittest.TestCase):
    """Tests pour l'enregistrement des types d'engrenages"""
    
    def setUp(self):
        """Préparer les tests - enregistrer les types"""
        # Nettoyer d'abord
        GearFactory._gear_types.clear()
        
        # Enregistrer tous les types
        GearFactory.register_gear('spur', SpurGear)
        GearFactory.register_gear('helical', HelicalGear)
        GearFactory.register_gear('bevel', BevelGear)
        GearFactory.register_gear('worm', WormGear)
        GearFactory.register_gear('rack', RackGear)
        GearFactory.register_gear('internal', InternalGear)
    
    def test_register_gear(self):
        """Test l'enregistrement d'un type d'engrenage"""
        self.assertIn('spur', GearFactory._gear_types)
        self.assertIn('helical', GearFactory._gear_types)
    
    def test_get_available_types(self):
        """Test l'obtention des types disponibles"""
        types = GearFactory.get_available_types()
        
        self.assertIn('spur', types)
        self.assertIn('helical', types)
        self.assertIn('bevel', types)
        self.assertIn('worm', types)
        self.assertIn('rack', types)
        self.assertIn('internal', types)
    
    def test_duplicate_registration(self):
        """Test que l'enregistrement en doublon remplace le précédent"""
        original_class = GearFactory._gear_types['spur']
        GearFactory.register_gear('spur', HelicalGear)
        
        self.assertNotEqual(GearFactory._gear_types['spur'], original_class)
        self.assertEqual(GearFactory._gear_types['spur'], HelicalGear)
        
        # Restaurer
        GearFactory.register_gear('spur', SpurGear)


class TestGearFactoryCreation(unittest.TestCase):
    """Tests pour la création d'engrenages"""
    
    def setUp(self):
        """Préparer les tests"""
        GearFactory._gear_types.clear()
        GearFactory.register_gear('spur', SpurGear)
        GearFactory.register_gear('helical', HelicalGear)
        GearFactory.register_gear('bevel', BevelGear)
    
    def test_create_spur_gear(self):
        """Test la création d'un engrenage droit"""
        params = GearParams(
            name="TestSpur",
            module=2.0,
            teeth=20
        )
        
        gear = GearFactory.create_gear('spur', params)
        
        self.assertIsInstance(gear, SpurGear)
        self.assertEqual(gear.params.name, "TestSpur")
        self.assertEqual(gear.params.module, 2.0)
    
    def test_create_helical_gear(self):
        """Test la création d'un engrenage hélicoïdal"""
        params = GearParams(
            name="TestHelical",
            module=2.0,
            teeth=20,
            helix_angle=15.0
        )
        
        gear = GearFactory.create_gear('helical', params)
        
        self.assertIsInstance(gear, HelicalGear)
        self.assertEqual(gear.params.helix_angle, 15.0)
    
    def test_create_with_invalid_type(self):
        """Test la création avec un type invalide"""
        params = GearParams(
            name="BadGear",
            module=2.0,
            teeth=20
        )
        
        with self.assertRaises(ValueError) as context:
            GearFactory.create_gear('invalid_type', params)
        
        self.assertIn('non supporté', str(context.exception))
    
    def test_create_with_case_insensitive(self):
        """Test que le type est case-insensitive"""
        params = GearParams(
            name="TestCase",
            module=2.0,
            teeth=20
        )
        
        gear1 = GearFactory.create_gear('SPUR', params)
        gear2 = GearFactory.create_gear('Spur', params)
        gear3 = GearFactory.create_gear('spur', params)
        
        self.assertIsInstance(gear1, SpurGear)
        self.assertIsInstance(gear2, SpurGear)
        self.assertIsInstance(gear3, SpurGear)
    
    def test_create_with_kwargs(self):
        """Test la création avec des kwargs"""
        params = GearParams(
            name="TestKwargs",
            module=2.0,
            teeth=20
        )
        
        gear = GearFactory.create_gear(
            'spur',
            params,
            pressure_angle=25.0,
            face_width=15.0
        )
        
        self.assertEqual(gear.params.pressure_angle, 25.0)
        self.assertEqual(gear.params.face_width, 15.0)


class TestGearFactoryFromDict(unittest.TestCase):
    """Tests pour la création à partir de dictionnaire"""
    
    def setUp(self):
        """Préparer les tests"""
        GearFactory._gear_types.clear()
        GearFactory.register_gear('spur', SpurGear)
        GearFactory.register_gear('helical', HelicalGear)
    
    def test_from_dict_spur(self):
        """Test la création depuis dictionnaire pour spur"""
        config = {
            'type': 'spur',
            'name': 'DictGear',
            'module': 2.0,
            'teeth': 25
        }
        
        gear = GearFactory.from_dict(config)
        
        self.assertIsInstance(gear, SpurGear)
        self.assertEqual(gear.params.name, 'DictGear')
        self.assertEqual(gear.params.module, 2.0)
    
    def test_from_dict_default_type(self):
        """Test la création avec type par défaut"""
        config = {
            'name': 'DefaultGear',
            'module': 1.5,
            'teeth': 20
        }
        
        gear = GearFactory.from_dict(config)
        
        self.assertIsInstance(gear, SpurGear)  # Type par défaut
    
    def test_from_dict_with_params(self):
        """Test la création avec clé 'params'"""
        config = {
            'type': 'helical',
            'params': {
                'name': 'ParamsGear',
                'module': 2.0,
                'teeth': 20,
                'helix_angle': 20.0
            }
        }
        
        gear = GearFactory.from_dict(config)
        
        self.assertIsInstance(gear, HelicalGear)
        self.assertEqual(gear.params.helix_angle, 20.0)


class TestGearFactoryIntegration(unittest.TestCase):
    """Tests d'intégration du factory"""
    
    def setUp(self):
        """Préparer les tests"""
        GearFactory._gear_types.clear()
        GearFactory.register_gear('spur', SpurGear)
        GearFactory.register_gear('helical', HelicalGear)
    
    def test_create_multiple_gears(self):
        """Test la création de plusieurs engrenages"""
        gears = []
        
        for i in range(5):
            params = GearParams(
                name=f"Gear{i}",
                module=2.0,
                teeth=15 + i * 5
            )
            gear = GearFactory.create_gear('spur', params)
            gears.append(gear)
        
        self.assertEqual(len(gears), 5)
        
        for i, gear in enumerate(gears):
            self.assertEqual(gear.params.teeth, 15 + i * 5)
    
    def test_gear_persistence(self):
        """Test que les engrenages créés conservent leurs propriétés"""
        params1 = GearParams(
            name="Gear1",
            module=2.0,
            teeth=20
        )
        
        params2 = GearParams(
            name="Gear2",
            module=3.0,
            teeth=30
        )
        
        gear1 = GearFactory.create_gear('spur', params1)
        gear2 = GearFactory.create_gear('spur', params2)
        
        # Vérifier que les engrenages ont leurs propres paramètres
        self.assertEqual(gear1.params.module, 2.0)
        self.assertEqual(gear2.params.module, 3.0)
        self.assertNotEqual(gear1.params.teeth, gear2.params.teeth)


if __name__ == '__main__':
    unittest.main()
