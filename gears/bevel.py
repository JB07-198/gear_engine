from core.base_gear import Gear, GearParams
from core.math_utils import GearMath
from typing import Dict, Any, Tuple
import math

class BevelGear(Gear):
    """Engrenage conique"""
    
    def __init__(self, params: GearParams):
        # Initialiser pitch_angle avant d'appeler super().__init__()
        self.shaft_angle = params.shaft_angle or 90.0
        
        # Calcul de l'angle primitif
        if params.pitch_angle is not None:
            self.pitch_angle = params.pitch_angle
        else:
            # Par défaut, pour un engrenage conique à axes orthogonaux
            if params.mate_teeth is not None:
                self.pitch_angle = math.degrees(
                    math.atan(params.teeth / params.mate_teeth)
                )
            else:
                # Angle par défaut pour 45 degrés (1:1)
                self.pitch_angle = 45.0
        
        self.back_angle = self.shaft_angle - self.pitch_angle
        
        super().__init__(params)
    
    def _calculate_geometry(self):
        """Calculer la géométrie spécifique aux engrenages coniques"""
        # Rayon primitif moyen (pour les calculs)
        self.mean_pitch_radius = self.pitch_diameter / 2 * math.cos(
            math.radians(self.pitch_angle)
        )
        
        # Hauteur du cône (distance du sommet à la ligne primitive)
        sin_pitch = math.sin(math.radians(self.pitch_angle))
        if sin_pitch > 0:
            self.cone_distance = self.pitch_diameter / (2 * sin_pitch)
        else:
            self.cone_distance = float('inf')
    
    def mesh_with(self, other: Gear) -> Tuple[float, float]:
        """Calculer les paramètres d'engrènement"""
        if not isinstance(other, BevelGear):
            raise ValueError("Un engrenage conique doit s'engrener avec un autre engrenage conique")
        
        # Pour engrenages coniques à axes orthogonaux
        if abs(self.pitch_angle + other.pitch_angle - 90) > 0.1:
            raise ValueError("La somme des angles de cône doit être 90° pour des axes orthogonaux")
        
        # Distance entre centres (approximation)
        center_distance = (self.cone_distance + other.cone_distance) / 2
        
        # Rapport de contact simplifié mais cohérent
        contact_ratio = 1.2 + 0.02 * min(
        self.params.teeth,
        other.params.teeth
    )
        
        return center_distance, contact_ratio
    
    @property
    def outside_diameter(self) -> float:
        """Diamètre extérieur (au grand bout)"""
        addendum = self.params.module
        return self.pitch_diameter + 2 * addendum * math.cos(
            math.radians(self.pitch_angle)
        )
    
    @property
    def root_diameter(self) -> float:
        """Diamètre de pied (au grand bout)"""
        dedendum = 1.25 * self.params.module
        return self.pitch_diameter - 2 * dedendum * math.cos(
            math.radians(self.pitch_angle)
        )
    
    @property
    def face_angle(self) -> float:
        """Angle de la face"""
        addendum_angle = math.degrees(math.atan(
            self.params.module / self.cone_distance
        ))
        return self.pitch_angle + addendum_angle
    
    @property
    def root_angle(self) -> float:
        """Angle de pied"""
        dedendum_angle = math.degrees(math.atan(
            1.25 * self.params.module / self.cone_distance
        ))
        return self.pitch_angle - dedendum_angle
    
    def get_info(self) -> Dict[str, Any]:
        """Informations spécifiques aux engrenages coniques"""
        info = super().get_info()
        info.update({
            'pitch_angle': self.pitch_angle,
            'back_angle': self.back_angle,
            'cone_distance': self.cone_distance,
            'mean_pitch_radius': self.mean_pitch_radius,
            'face_angle': self.face_angle,
            'root_angle': self.root_angle,
            'gear_type': 'bevel'
        })
        return info