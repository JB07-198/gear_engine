from core.base_gear import Gear, GearParams
from core.math_utils import GearMath
from profiles.involute import InvoluteProfile
from typing import Dict, Any, Tuple, List
import math

class RackGear(Gear):
    """Crémaillère"""
    
    def _calculate_geometry(self):
        """Calculer la géométrie spécifique aux crémaillères"""
        self.profile = InvoluteProfile(self.params.pressure_angle)
        
        # Une crémaillère a essentiellement un rayon infini
        self.pitch_line_height = 0  # Par convention
    
    def mesh_with(self, other: Gear) -> Tuple[float, float]:
        """Calculer les paramètres d'engrènement avec un pignon"""
        from .spur import SpurGear
        
        if not isinstance(other, SpurGear):
            raise ValueError("Une crémaillère s'engrène avec un pignon droit")
        
        # Distance entre la ligne primitive et le centre du pignon
        center_distance = other.pitch_diameter / 2
        
        # Pour une crémaillère (ligne primitive infinie), utiliser
        # l'estimation du rapport de contact du pignon seul
        contact_ratio = other.contact_ratio if hasattr(other, 'contact_ratio') else 0.0

        return center_distance, contact_ratio
    
    @property
    def pitch_diameter(self) -> float:
        """Diamètre primitif (infini pour une crémaillère)"""
        return float('inf')
    
    @property
    def tooth_height(self) -> float:
        """Hauteur totale de la dent"""
        return 2.25 * self.params.module
    
    @property
    def tooth_thickness(self) -> float:
        """Épaisseur de la dent sur la ligne primitive"""
        return math.pi * self.params.module / 2
    
    def get_tooth_profile(self) -> List[Tuple[float, float]]:
        """Profil de dent de crémaillère (trapézoïdal)"""
        # Points pour une dent de crémaillère
        p = self.params.module * math.pi  # Pas
        h_a = self.params.module  # Hauteur de tête
        h_f = 1.25 * self.params.module  # Hauteur de pied
        
        points = [
            (-p/4, -h_f),           # Point bas gauche
            (-p/4 + self.tooth_thickness, -h_f),  # Point bas droit
            (-p/4 + self.tooth_thickness + h_a * math.tan(
                math.radians(self.params.pressure_angle)), h_a),  # Point haut droit
            (-p/4 - h_a * math.tan(
                math.radians(self.params.pressure_angle)), h_a),   # Point haut gauche
            (-p/4, -h_f)            # Retour au point bas gauche
        ]
        
        return points
    
    def get_info(self) -> Dict[str, Any]:
        """Informations spécifiques aux crémaillères"""
        info = super().get_info()
        info.update({
            'tooth_height': self.tooth_height,
            'tooth_thickness': self.tooth_thickness,
            'circular_pitch': math.pi * self.params.module,
            'gear_type': 'rack'
        })
        return info