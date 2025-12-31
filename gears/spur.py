from core.base_gear import Gear, GearParams
from core.math_utils import GearMath
from profiles.involute import InvoluteProfile
from typing import Dict, Any, Tuple
import math

class SpurGear(Gear):
    """Engrenage cylindrique à denture droite"""
    
    def _calculate_geometry(self):
        """Calculer la géométrie spécifique aux engrenages droits"""
        self.profile = InvoluteProfile(self.params.pressure_angle)
        
        # Calcul du déport si nécessaire
        if self.params.teeth < 17 and self.params.profile_shift == 0:
            self.params.profile_shift = GearMath.profile_shift_coefficient(
                self.params.teeth, self.params.pressure_angle
            )
    
    def mesh_with(self, other: Gear) -> Tuple[float, float]:
        """Calculer les paramètres d'engrènement"""
        if not isinstance(other, SpurGear):
            raise ValueError("Un engrenage droit ne peut s'engrener qu'avec un autre engrenage droit")
        
        # Distance entre centres
        center_distance = GearMath.center_distance(self, other)
        
        # Rapport de contact
        contact_ratio = GearMath.contact_ratio_base_path(self, other, self.params.pressure_angle)
        
        return center_distance, contact_ratio
    
    @property
    def base_diameter(self) -> float:
        """Diamètre de base"""
        return GearMath.base_diameter(self.pitch_diameter, self.params.pressure_angle)
    
    @property
    def circular_pitch(self) -> float:
        """Pas circonférentiel"""
        return math.pi * self.params.module
    
    @property
    def contact_ratio(self) -> float:
        """Rapport de contact estimé"""
        # Valeur par défaut pour un engrenage droit standard
        return 1.4 + (self.params.teeth / 100)
    
    def get_tooth_points(self, num_points: int = 50) -> list:
        """Générer les points d'une dent"""
        base_radius = self.base_diameter / 2
        pitch_radius = self.pitch_diameter / 2
        
        # Points de la développante
        points = self.profile.generate_points(
            base_radius,
            start_angle=0,
            end_angle=60,
            num_points=num_points
        )
        
        return points
    
    def get_info(self) -> Dict[str, Any]:
        """Informations spécifiques aux engrenages droits"""
        info = super().get_info()
        info.update({
            'base_diameter': self.base_diameter,
            'circular_pitch': self.circular_pitch,
            'contact_ratio': self.contact_ratio,
            'profile_shift': self.params.profile_shift,
            'gear_type': 'spur'
        })
        return info