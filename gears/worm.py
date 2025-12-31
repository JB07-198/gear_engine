from core.base_gear import Gear, GearParams
from typing import Dict, Any, Tuple
import math

class WormGear(Gear):
    """Vis sans fin"""
    
    def __init__(self, params: GearParams, worm_diameter: float = None):
        # Initialiser leads avant super().__init__() pour l'utiliser dans _calculate_geometry
        self.leads = params.leads if params.leads is not None else 1
        self.worm_diameter = worm_diameter or (params.module * 10)
        super().__init__(params)
    
    def _calculate_geometry(self):
        """Calculer la géométrie spécifique aux vis sans fin"""
        # Pas axial
        self.axial_pitch = math.pi * self.params.module
        
        # Pas de la vis
        self.lead = self.leads * self.axial_pitch
        
        # Angle d'hélice de la vis
        self.lead_angle = math.degrees(math.atan(
            self.lead / (math.pi * self.worm_diameter)
        ))
    
    def mesh_with(self, other: Gear) -> Tuple[float, float]:
        """Calculer les paramètres d'engrènement avec une roue"""
        from .spur import SpurGear
        
        if not isinstance(other, SpurGear):
            raise ValueError("Une vis sans fin s'engrène avec une roue droite")
        
        # Distance entre centres
        center_distance = (self.worm_diameter + other.pitch_diameter) / 2
        
        # Rapport de réduction
        reduction_ratio = other.params.teeth / self.leads
        
        return center_distance, reduction_ratio
    
    @property
    def pitch_diameter(self) -> float:
        """Diamètre primitif de la vis"""
        return self.worm_diameter
    
    @property
    def outside_diameter(self) -> float:
        """Diamètre extérieur de la vis"""
        return self.worm_diameter + 2 * self.params.module
    
    @property
    def root_diameter(self) -> float:
        """Diamètre de pied de la vis"""
        return self.worm_diameter - 2 * 1.25 * self.params.module
    
    def sliding_velocity(self, rpm: float) -> float:
        """Vitesse de glissement"""
        pitch_line_velocity = math.pi * self.worm_diameter * rpm / 60
        return pitch_line_velocity / math.cos(math.radians(self.lead_angle))
    
    def efficiency(self, friction_coefficient: float = 0.05) -> float:
        """Rendement estimé"""
        lambda_rad = math.radians(self.lead_angle)
        mu = friction_coefficient
        
        efficiency = math.cos(lambda_rad) - mu * math.tan(lambda_rad)
        efficiency /= math.cos(lambda_rad) + mu / math.tan(lambda_rad)
        
        return max(0, min(1, efficiency))
    
    def get_info(self) -> Dict[str, Any]:
        """Informations spécifiques aux vis sans fin"""
        info = super().get_info()
        info.update({
            'leads': self.leads,
            'worm_diameter': self.worm_diameter,
            'axial_pitch': self.axial_pitch,
            'lead': self.lead,
            'lead_angle': self.lead_angle,
            'gear_type': 'worm'
        })
        return info