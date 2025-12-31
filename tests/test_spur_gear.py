"""
Tests pour la classe SpurGear
"""
import unittest
import math
from core.base_gear import GearParams
from gears.spur import SpurGear


class TestSpurGearAdvanced(unittest.TestCase):
    """Tests avancés pour SpurGear"""
    
    def test_small_gear_profile_shift(self):
        """Test le déport de profil pour petits engrenages"""
        # Un engrenage avec moins de 17 dents devrait avoir un déport
        params = GearParams(
            name="SmallGear",
            module=2.0,
            teeth=14,  # Moins de 17
            pressure_angle=20.0,
            profile_shift=0.0
        )
        gear = SpurGear(params)
        
        # Après la création, le déport doit être calculé
        self.assertGreater(gear.params.profile_shift, 0)
    
    def test_large_gear_no_shift(self):
        """Test qu'un grand engrenage ne needs pas de déport"""
        params = GearParams(
            name="LargeGear",
            module=2.0,
            teeth=30,
            pressure_angle=20.0,
            profile_shift=0.0
        )
        gear = SpurGear(params)
        
        # Aucun déport pour un grand engrenage
        self.assertEqual(gear.params.profile_shift, 0.0)
    
    def test_tooth_points_generation(self):
        """Test la génération des points de dent"""
        params = GearParams(
            name="TestGear",
            module=2.0,
            teeth=20
        )
        gear = SpurGear(params)
        
        points = gear.get_tooth_points(num_points=50)
        
        self.assertEqual(len(points), 50)
        # Vérifier que les points sont des tuples (x, y)
        for point in points:
            self.assertIsInstance(point, tuple)
            self.assertEqual(len(point), 2)
    
    def test_different_pressure_angles(self):
        """Tester des engrenages avec différents angles de pression"""
        for angle in [14.0, 20.0, 25.0]:
            params = GearParams(
                name=f"Gear_{angle}",
                module=2.0,
                teeth=20,
                pressure_angle=angle
            )
            gear = SpurGear(params)
            
            # Le diamètre de base dépend de l'angle de pression
            expected_base = gear.pitch_diameter * math.cos(math.radians(angle))
            self.assertAlmostEqual(gear.base_diameter, expected_base, places=3)
    
    def test_mesh_with_different_teeth(self):
        """Tester l'engrènement avec des nombres de dents différents"""
        gear1 = SpurGear(GearParams(
            name="Pinion",
            module=2.0,
            teeth=15
        ))
        
        gear2 = SpurGear(GearParams(
            name="Wheel",
            module=2.0,
            teeth=40
        ))
        
        center_distance, contact_ratio = gear1.mesh_with(gear2)
        
        expected_distance = (gear1.pitch_diameter + gear2.pitch_diameter) / 2
        self.assertEqual(center_distance, expected_distance)
        
        # Le rapport de contact dépend du nombre de dents
        self.assertGreater(contact_ratio, 0)


class TestSpurGearCalculations(unittest.TestCase):
    """Tests des calculs géométriques"""
    
    def setUp(self):
        """Préparer les tests"""
        self.params = GearParams(
            name="TestGear",
            module=2.0,
            teeth=20,
            pressure_angle=20.0,
            face_width=10.0
        )
        self.gear = SpurGear(self.params)
    
    def test_pitch_calculations(self):
        """Tester les calculs de pas"""
        # Pas circonférentiel
        circular_pitch = self.gear.circular_pitch
        self.assertAlmostEqual(circular_pitch, math.pi * 2.0, places=3)
    
    def test_geometric_proportions(self):
        """Tester les proportions géométriques"""
        pitch_d = self.gear.pitch_diameter
        outside_d = self.gear.outside_diameter
        root_d = self.gear.root_diameter
        
        # Le diamètre extérieur doit être supérieur au diamètre primitif
        self.assertGreater(outside_d, pitch_d)
        
        # Le diamètre de pied doit être inférieur au diamètre primitif
        self.assertLess(root_d, pitch_d)
        
        # Vérifier les différences
        addendum_check = outside_d - pitch_d
        dedendum_check = pitch_d - root_d
        
        self.assertAlmostEqual(addendum_check, 2 * self.gear.addendum, places=3)
        self.assertAlmostEqual(dedendum_check, 2 * self.gear.dedendum, places=3)


class TestSpurGearInfo(unittest.TestCase):
    """Tests de la méthode get_info"""
    
    def test_info_complete(self):
        """Tester que les infos contiennent tous les éléments nécessaires"""
        params = GearParams(
            name="InfoTest",
            module=1.5,
            teeth=25,
            pressure_angle=20.0,
            face_width=8.0
        )
        gear = SpurGear(params)
        info = gear.get_info()
        
        required_keys = [
            'name', 'type', 'module', 'teeth', 'pitch_diameter',
            'outside_diameter', 'root_diameter', 'addendum', 'dedendum',
            'face_width', 'base_diameter', 'circular_pitch', 'contact_ratio',
            'profile_shift', 'gear_type'
        ]
        
        for key in required_keys:
            self.assertIn(key, info, f"Clé manquante: {key}")
    
    def test_info_values_accuracy(self):
        """Tester la précision des valeurs dans get_info"""
        params = GearParams(
            name="AccuracyTest",
            module=3.0,
            teeth=16,
            face_width=12.0
        )
        gear = SpurGear(params)
        info = gear.get_info()
        
        self.assertEqual(info['module'], 3.0)
        self.assertEqual(info['teeth'], 16)
        self.assertEqual(info['face_width'], 12.0)
        self.assertEqual(info['name'], "AccuracyTest")


if __name__ == '__main__':
    unittest.main()
