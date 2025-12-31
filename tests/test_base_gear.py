"""
Tests pour les classes de base des engrenages
"""
import unittest
import math
from core.base_gear import Gear, GearParams
from gears.spur import SpurGear


class TestGearParams(unittest.TestCase):
    """Tests pour la classe GearParams"""
    
    def test_valid_params(self):
        """Test la création de paramètres valides"""
        params = GearParams(
            name="TestGear",
            module=2.0,
            teeth=20,
            pressure_angle=20.0
        )
        self.assertEqual(params.name, "TestGear")
        self.assertEqual(params.module, 2.0)
        self.assertEqual(params.teeth, 20)
        self.assertEqual(params.pressure_angle, 20.0)
    
    def test_invalid_module(self):
        """Test la validation du module négatif"""
        params = GearParams(
            name="BadGear",
            module=-1.0,
            teeth=20
        )
        with self.assertRaises(ValueError):
            params.validate()
    
    def test_invalid_teeth(self):
        """Test la validation du nombre de dents zéro"""
        params = GearParams(
            name="BadGear",
            module=2.0,
            teeth=0
        )
        with self.assertRaises(ValueError):
            params.validate()
    
    def test_invalid_pressure_angle(self):
        """Test la validation de l'angle de pression"""
        params = GearParams(
            name="BadGear",
            module=2.0,
            teeth=20,
            pressure_angle=30.0
        )
        with self.assertRaises(ValueError):
            params.validate()


class TestSpurGear(unittest.TestCase):
    """Tests pour la classe SpurGear"""
    
    def setUp(self):
        """Préparer les tests"""
        self.params = GearParams(
            name="TestGear",
            module=2.0,
            teeth=20,
            pressure_angle=20.0
        )
        self.gear = SpurGear(self.params)
    
    def test_pitch_diameter(self):
        """Test le calcul du diamètre primitif"""
        expected = 2.0 * 20  # module * teeth
        self.assertEqual(self.gear.pitch_diameter, expected)
    
    def test_outside_diameter(self):
        """Test le calcul du diamètre extérieur"""
        expected = self.gear.pitch_diameter + 2 * self.gear.addendum
        self.assertEqual(self.gear.outside_diameter, expected)
    
    def test_root_diameter(self):
        """Test le calcul du diamètre de pied"""
        expected = self.gear.pitch_diameter - 2 * self.gear.dedendum
        self.assertEqual(self.gear.root_diameter, expected)
    
    def test_addendum(self):
        """Test le calcul de la hauteur de tête"""
        self.assertEqual(self.gear.addendum, self.params.module)
    
    def test_dedendum(self):
        """Test le calcul de la hauteur de pied"""
        self.assertEqual(self.gear.dedendum, 1.25 * self.params.module)
    
    def test_base_diameter(self):
        """Test le calcul du diamètre de base"""
        expected = self.gear.pitch_diameter * math.cos(math.radians(20.0))
        self.assertAlmostEqual(self.gear.base_diameter, expected, places=3)
    
    def test_circular_pitch(self):
        """Test le calcul du pas circonférentiel"""
        expected = math.pi * self.params.module
        self.assertAlmostEqual(self.gear.circular_pitch, expected, places=3)
    
    def test_contact_ratio(self):
        """Test le rapport de contact"""
        self.assertGreater(self.gear.contact_ratio, 1.0)
        self.assertLess(self.gear.contact_ratio, 2.0)
    
    def test_get_info(self):
        """Test les informations de l'engrenage"""
        info = self.gear.get_info()
        
        self.assertEqual(info['name'], "TestGear")
        self.assertEqual(info['type'], "SpurGear")
        self.assertEqual(info['module'], 2.0)
        self.assertEqual(info['teeth'], 20)
        self.assertEqual(info['gear_type'], 'spur')
        self.assertIn('pitch_diameter', info)
        self.assertIn('outside_diameter', info)
        self.assertIn('contact_ratio', info)
    
    def test_mesh_with_same_type(self):
        """Test l'engrènement de deux engrenages droits"""
        gear2 = SpurGear(GearParams(
            name="Gear2",
            module=2.0,
            teeth=30,
            pressure_angle=20.0
        ))
        
        center_distance, contact_ratio = self.gear.mesh_with(gear2)
        
        expected_distance = (self.gear.pitch_diameter + gear2.pitch_diameter) / 2
        self.assertEqual(center_distance, expected_distance)
        self.assertGreater(contact_ratio, 0)
    
    def test_mesh_with_wrong_type(self):
        """Test l'engrènement avec un mauvais type"""
        from gears.helical import HelicalGear
        
        helical_params = GearParams(
            name="HelicalGear",
            module=2.0,
            teeth=20,
            helix_angle=15.0
        )
        helical = HelicalGear(helical_params)
        
        with self.assertRaises(ValueError):
            self.gear.mesh_with(helical)
    
    def test_string_representation(self):
        """Test la représentation en chaîne"""
        str_repr = str(self.gear)
        self.assertIn("SpurGear", str_repr)
        self.assertIn("TestGear", str_repr)
        self.assertIn("m=2.0", str_repr)
        self.assertIn("z=20", str_repr)


class TestGearGeometry(unittest.TestCase):
    """Tests de la géométrie des engrenages"""
    
    def test_different_modules(self):
        """Tester des engrenages avec différents modules"""
        for module in [1.0, 1.5, 2.0, 3.0]:
            params = GearParams(
                name=f"Gear_{module}",
                module=module,
                teeth=20
            )
            gear = SpurGear(params)
            
            self.assertEqual(gear.pitch_diameter, module * 20)
            self.assertEqual(gear.addendum, module)
    
    def test_different_teeth(self):
        """Tester des engrenages avec différent nombre de dents"""
        for teeth in [12, 20, 30, 50]:
            params = GearParams(
                name=f"Gear_{teeth}",
                module=2.0,
                teeth=teeth
            )
            gear = SpurGear(params)
            
            self.assertEqual(gear.pitch_diameter, 2.0 * teeth)


if __name__ == '__main__':
    unittest.main()
