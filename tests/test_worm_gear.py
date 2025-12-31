import pytest
from core.base_gear import GearParams
from gears.worm import WormGear
from gears.spur import SpurGear
import math

class TestWormGearCreation:
    """Tests pour la création de vis sans fin (Test 14)"""
    
    def test_worm_gear_creation_basic(self):
        """Test 14.1 : Créer une vis sans fin avec paramètres de base"""
        params = GearParams(
            name="Worm1",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        worm = WormGear(params)
        
        assert worm is not None
        assert worm.params.name == "Worm1"
        assert worm.params.module == 2.0
        assert worm.params.teeth == 1
        assert worm.leads == 1
    
    def test_worm_gear_creation_with_multiple_leads(self):
        """Test 14.2 : Créer une vis sans fin avec plusieurs filetages"""
        params = GearParams(
            name="Worm2",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=3
        )
        worm = WormGear(params)
        
        assert worm.leads == 3
    
    def test_worm_gear_default_leads(self):
        """Test 14.3 : Vis sans fin avec leads non défini (défaut = 1)"""
        params = GearParams(
            name="Worm3",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0
        )
        worm = WormGear(params)
        
        assert worm.leads == 1
    
    def test_worm_gear_pitch_diameter(self):
        """Test 14.4 : Diamètre primitif de la vis sans fin"""
        params = GearParams(
            name="Worm4",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        worm = WormGear(params)
        
        # Diamètre primitif = module * 10
        expected_diameter = 2.0 * 10
        assert abs(worm.pitch_diameter - expected_diameter) < 0.01
    
    def test_worm_gear_outside_diameter(self):
        """Test 14.5 : Diamètre extérieur de la vis sans fin"""
        params = GearParams(
            name="Worm5",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        worm = WormGear(params)
        
        # Diamètre extérieur = diamètre primitif + 2 * module
        expected_outside = (2.0 * 10) + (2 * 2.0)
        assert abs(worm.outside_diameter - expected_outside) < 0.01
    
    def test_worm_gear_root_diameter(self):
        """Test 14.6 : Diamètre de pied de la vis sans fin"""
        params = GearParams(
            name="Worm6",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        worm = WormGear(params)
        
        # Diamètre de pied = diamètre primitif - 2 * 1.25 * module
        expected_root = (2.0 * 10) - (2 * 1.25 * 2.0)
        assert abs(worm.root_diameter - expected_root) < 0.01
    
    def test_worm_gear_axial_pitch(self):
        """Test 14.7 : Pas axial de la vis sans fin"""
        params = GearParams(
            name="Worm7",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        worm = WormGear(params)
        
        expected_pitch = math.pi * 2.0
        assert abs(worm.axial_pitch - expected_pitch) < 0.01
    
    def test_worm_gear_lead(self):
        """Test 14.8 : Pas de la vis sans fin"""
        params = GearParams(
            name="Worm8",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=2
        )
        worm = WormGear(params)
        
        # Lead = nombre de filetages * pas axial
        expected_lead = 2 * math.pi * 2.0
        assert abs(worm.lead - expected_lead) < 0.01
    
    def test_worm_gear_lead_angle(self):
        """Test 14.9 : Angle d'hélice de la vis sans fin"""
        params = GearParams(
            name="Worm9",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        worm = WormGear(params)
        
        # lead_angle doit être calculé
        assert hasattr(worm, 'lead_angle')
        assert 0 < worm.lead_angle < 90
    
    def test_worm_gear_mesh_with_spur(self):
        """Test 14.10 : Engrènement entre vis sans fin et engrenage droit"""
        worm_params = GearParams(
            name="Worm10",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        worm = WormGear(worm_params)
        
        spur_params = GearParams(
            name="SpurGear10",
            module=2.0,
            teeth=20,
            pressure_angle=20.0,
            face_width=10.0
        )
        spur = SpurGear(spur_params)
        
        center_distance, reduction_ratio = worm.mesh_with(spur)
        
        # Vérifier que les valeurs sont calculées
        assert center_distance > 0
        assert reduction_ratio == 20  # teeth / leads = 20 / 1
    
    def test_worm_gear_mesh_with_multiple_leads(self):
        """Test 14.11 : Engrènement avec plusieurs filetages"""
        worm_params = GearParams(
            name="Worm11",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=3
        )
        worm = WormGear(worm_params)
        
        spur_params = GearParams(
            name="SpurGear11",
            module=2.0,
            teeth=30,
            pressure_angle=20.0,
            face_width=10.0
        )
        spur = SpurGear(spur_params)
        
        center_distance, reduction_ratio = worm.mesh_with(spur)
        
        # Réduction = 30 / 3 = 10
        assert reduction_ratio == 10
    
    def test_worm_gear_sliding_velocity(self):
        """Test 14.12 : Calcul de la vitesse de glissement"""
        params = GearParams(
            name="Worm12",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        worm = WormGear(params)
        
        # Vitesse de glissement à 1000 tr/min
        velocity = worm.sliding_velocity(1000)
        assert velocity > 0
    
    def test_worm_gear_efficiency(self):
        """Test 14.13 : Calcul du rendement"""
        params = GearParams(
            name="Worm13",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        worm = WormGear(params)
        
        efficiency = worm.efficiency()
        # Rendement doit être entre 0 et 1
        assert 0 <= efficiency <= 1
    
    def test_worm_gear_get_info(self):
        """Test 14.14 : Récupérer les informations complètes de la vis sans fin"""
        params = GearParams(
            name="Worm14",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=2
        )
        worm = WormGear(params)
        
        info = worm.get_info()
        
        # Vérifier que les informations WormGear-spécifiques sont présentes
        assert 'leads' in info
        assert 'worm_diameter' in info
        assert 'axial_pitch' in info
        assert 'lead' in info
        assert 'lead_angle' in info
        assert info['leads'] == 2
    
    def test_worm_gear_mesh_invalid_partner(self):
        """Test 14.15 : Erreur si engrènement avec type incompatible"""
        worm_params = GearParams(
            name="Worm15",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        worm = WormGear(worm_params)
        
        # Essayer d'engrener avec un autre WormGear (invalide)
        other_worm_params = GearParams(
            name="Worm15b",
            module=2.0,
            teeth=1,
            pressure_angle=20.0,
            face_width=10.0,
            leads=1
        )
        other_worm = WormGear(other_worm_params)
        
        with pytest.raises(ValueError):
            worm.mesh_with(other_worm)
