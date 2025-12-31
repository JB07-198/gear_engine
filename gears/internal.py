from core.base_gear import Gear, GearParams
from core.math_utils import GearMath
from profiles.involute import InvoluteProfile
from typing import Dict, Any, Tuple
import math

class InternalGear(Gear):
    """Engrenage intérieur"""
    
    def _calculate_geometry(self):
        """Calculer la géométrie spécifique aux engrenages intérieurs"""
        self.profile = InvoluteProfile(self.params.pressure_angle)
        
        # Pour engrenages intérieurs, certaines formules sont inversées
        if self.params.teeth < 32:
            # Déport recommandé pour éviter l'interférence
            self.params.profile_shift = 0.5
    
    def mesh_with(self, other: Gear) -> Tuple[float, float]:
        """Calculer les paramètres d'engrènement avec un pignon extérieur"""
        from .spur import SpurGear
        
        if not isinstance(other, SpurGear):
            raise ValueError("Un engrenage intérieur s'engrène avec un pignon extérieur")
        
        if other.params.teeth >= self.params.teeth:
            raise ValueError("Le pignon doit avoir moins de dents que l'engrenage intérieur")
        
        # Distance entre centres (négative car intérieur)
        center_distance = (self.pitch_diameter - other.pitch_diameter) / 2
        
        # Rapport de contact (simplifié)
        contact_ratio = GearMath.contact_ratio_base_path(self, other, self.params.pressure_angle)

        # Pour engrenages intérieurs la valeur peut être négative selon la géométrie;
        # clamper à 0 pour indiquer absence de contact si négatif.
        contact_ratio = max(0.0, contact_ratio)

        return center_distance, contact_ratio
    
    @property
    def outside_diameter(self) -> float:
        """Diamètre extérieur (intérieur de la couronne)"""
        return self.pitch_diameter - 2 * self.params.module
    
    @property
    def root_diameter(self) -> float:
        """Diamètre de pied (extérieur de la couronne)"""
        return self.pitch_diameter + 2 * 1.25 * self.params.module
    
    @property
    def base_diameter(self) -> float:
        """Diamètre de base"""
        return GearMath.base_diameter(self.pitch_diameter, self.params.pressure_angle)
    
    def check_interference(self, pinion_teeth: int) -> bool:
        """Vérifier l'interférence avec un pignon"""
        # Condition d'interférence pour engrenages intérieurs
        alpha = math.radians(self.params.pressure_angle)
        
        # Nombre minimum de dents du pignon
        z1_min = (2 * self.params.teeth * math.sin(alpha)**2) / \
                 (self.params.teeth * math.sin(alpha)**2 - 2)
        
        return pinion_teeth < z1_min
    
    def get_info(self) -> Dict[str, Any]:
        """Informations spécifiques aux engrenages intérieurs"""
        info = super().get_info()
        info.update({
            'base_diameter': self.base_diameter,
            'gear_type': 'internal',
            'is_internal': True
        })
        return info