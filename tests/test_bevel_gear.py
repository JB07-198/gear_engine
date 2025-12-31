"""
Tests spécifiques pour BevelGear (Test 13)
"""
import unittest
import math
from core.base_gear import GearParams
from gears.bevel import BevelGear


class TestBevelGear(unittest.TestCase):
    """Tests pour BevelGear (Test 13)"""
    
    def test_bevel_gear_creation(self):
        """Test la création d'un engrenage conique"""
        params = GearParams(
            name="BevelTest",
            module=2.0,
            teeth=24,
            pressure_angle=20.0,
            face_width=12.0,
            pitch_angle=45.0,
            shaft_angle=90.0
        )
        
        gear = BevelGear(params)
        
        self.assertEqual(gear.params.name, "BevelTest")
        self.assertEqual(gear.params.module, 2.0)
        self.assertEqual(gear.params.teeth, 24)
        self.assertEqual(gear.pitch_angle, 45.0)
        self.assertEqual(gear.shaft_angle, 90.0)
    
    def test_bevel_gear_pitch_angle_calculation(self):
        """Test le calcul automatique de l'angle de pas"""
        # Sans pitch_angle, en utilisant mate_teeth
        params = GearParams(
            name="BevelAuto",
            module=2.0,
            teeth=20,
            mate_teeth=20,  # Engrenage 1:1
            pressure_angle=20.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        # Pour un engrenage 1:1, l'angle doit être proche de 45°
        self.assertAlmostEqual(gear.pitch_angle, 45.0, places=1)
    
    def test_bevel_gear_default_pitch_angle(self):
        """Test l'angle par défaut sans mate_teeth ni pitch_angle"""
        params = GearParams(
            name="BevelDefault",
            module=2.0,
            teeth=24,
            pressure_angle=20.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        # Par défaut, 45°
        self.assertEqual(gear.pitch_angle, 45.0)
    
    def test_bevel_gear_back_angle(self):
        """Test le calcul de l'angle arrière"""
        params = GearParams(
            name="BevelBackAngle",
            module=2.0,
            teeth=24,
            pitch_angle=45.0,
            shaft_angle=90.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        # back_angle = shaft_angle - pitch_angle = 90 - 45 = 45
        self.assertEqual(gear.back_angle, 45.0)
    
    def test_bevel_gear_cone_distance(self):
        """Test le calcul de la distance de cône"""
        params = GearParams(
            name="BevelCone",
            module=2.0,
            teeth=24,
            pitch_angle=45.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        # cone_distance = pitch_diameter / (2 * sin(pitch_angle))
        # pitch_diameter = 2 * 24 = 48
        # sin(45°) = √2/2 ≈ 0.707
        # cone_distance = 48 / (2 * 0.707) ≈ 33.94
        self.assertAlmostEqual(gear.cone_distance, 33.94, places=1)
    
    def test_bevel_gear_mean_pitch_radius(self):
        """Test le rayon primitif moyen"""
        params = GearParams(
            name="BevelMeanRadius",
            module=2.0,
            teeth=24,
            pitch_angle=45.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        # mean_pitch_radius = pitch_diameter / 2 * cos(pitch_angle)
        # = 48 / 2 * cos(45°) = 24 * 0.707 ≈ 16.97
        self.assertAlmostEqual(gear.mean_pitch_radius, 16.97, places=1)
    
    def test_bevel_gear_pitch_diameter(self):
        """Test le diamètre primitif"""
        params = GearParams(
            name="BevelPitchDia",
            module=2.0,
            teeth=24,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        # pitch_diameter = module * teeth = 2.0 * 24 = 48
        self.assertEqual(gear.pitch_diameter, 48.0)
    
    def test_bevel_gear_outside_diameter(self):
        """Test le diamètre extérieur"""
        params = GearParams(
            name="BevelOutDia",
            module=2.0,
            teeth=24,
            pitch_angle=45.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        # outside_diameter = pitch_diameter + 2 * addendum * cos(pitch_angle)
        # = 48 + 2 * 2.0 * cos(45°) = 48 + 4 * 0.707 ≈ 50.83
        self.assertAlmostEqual(gear.outside_diameter, 50.83, places=1)
    
    def test_bevel_gear_root_diameter(self):
        """Test le diamètre de pied"""
        params = GearParams(
            name="BevelRootDia",
            module=2.0,
            teeth=24,
            pitch_angle=45.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        # root_diameter = pitch_diameter - 2 * dedendum * cos(pitch_angle)
        # = 48 - 2 * 2.5 * cos(45°) = 48 - 5 * 0.707 ≈ 44.46
        self.assertAlmostEqual(gear.root_diameter, 44.46, places=1)
    
    def test_bevel_gear_face_angle(self):
        """Test l'angle de face"""
        params = GearParams(
            name="BevelFaceAngle",
            module=2.0,
            teeth=24,
            pitch_angle=45.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        # face_angle = pitch_angle + addendum_angle
        # addendum_angle = atan(module / cone_distance)
        # = atan(2.0 / 33.94) ≈ 3.37°
        # face_angle ≈ 45 + 3.37 = 48.37°
        self.assertGreater(gear.face_angle, 45.0)
        self.assertLess(gear.face_angle, 50.0)
    
    def test_bevel_gear_root_angle(self):
        """Test l'angle de pied"""
        params = GearParams(
            name="BevelRootAngle",
            module=2.0,
            teeth=24,
            pitch_angle=45.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        # root_angle = pitch_angle - dedendum_angle
        self.assertLess(gear.root_angle, 45.0)
        self.assertGreater(gear.root_angle, 40.0)
    
    def test_bevel_gear_get_info(self):
        """Test la méthode get_info"""
        params = GearParams(
            name="BevelInfo",
            module=2.0,
            teeth=24,
            pitch_angle=45.0,
            shaft_angle=90.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        info = gear.get_info()
        
        # Vérifier que toutes les clés requises sont présentes
        required_keys = [
            'name', 'type', 'module', 'teeth', 'pitch_diameter',
            'outside_diameter', 'root_diameter', 'addendum', 'dedendum',
            'face_width', 'pitch_angle', 'back_angle', 'cone_distance',
            'mean_pitch_radius', 'face_angle', 'root_angle', 'gear_type'
        ]
        
        for key in required_keys:
            self.assertIn(key, info, f"Clé manquante: {key}")
        
        self.assertEqual(info['gear_type'], 'bevel')
    
    def test_bevel_gear_mesh_with_bevel(self):
        """Test l'engrènement de deux engrenages coniques"""
        params1 = GearParams(
            name="BevelPinion",
            module=2.0,
            teeth=24,
            pitch_angle=45.0,
            shaft_angle=90.0,
            face_width=12.0
        )
        
        params2 = GearParams(
            name="BevelWheel",
            module=2.0,
            teeth=24,
            pitch_angle=45.0,
            shaft_angle=90.0,
            face_width=12.0
        )
        
        gear1 = BevelGear(params1)
        gear2 = BevelGear(params2)
        
        center_distance, contact_ratio = gear1.mesh_with(gear2)
        
        self.assertGreater(center_distance, 0)
        self.assertGreater(contact_ratio, 0)
    
    def test_bevel_gear_cli_command(self):
        """Test la commande CLI pour créer un BevelGear"""
        # Ceci simule la commande:
        # python main.py create --type bevel --module 2 --teeth 24 --pitch-angle 45 --face-width 12
        
        params = GearParams(
            name="CLIBevelGear",
            module=2.0,
            teeth=24,
            pressure_angle=20.0,
            pitch_angle=45.0,
            shaft_angle=90.0,
            face_width=12.0
        )
        
        gear = BevelGear(params)
        
        self.assertIsInstance(gear, BevelGear)
        self.assertEqual(gear.params.name, "CLIBevelGear")


if __name__ == '__main__':
    unittest.main()
