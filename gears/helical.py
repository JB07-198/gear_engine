from core.base_gear import Gear, GearParams
from core.math_utils import GearMath
from profiles.involute import InvoluteProfile
from typing import Dict, Any, Tuple
import math

class HelicalGear(Gear):
    """Engrenage cylindrique à denture hélicoïdale"""
    
    def _calculate_geometry(self):
        """Calculer la géométrie spécifique aux engrenages hélicoïdaux"""
        self.profile = InvoluteProfile(self.params.pressure_angle)
        
        # Module apparent
        self.transverse_module = GearMath.transverse_module(
            self.params.module, self.params.helix_angle
        )
        
        # Pas axial
        self.axial_pitch = GearMath.axial_pitch(
            self.params.module, self.params.helix_angle
        )
    
    def mesh_with(self, other: Gear) -> Tuple[float, float]:
        """Calculer les paramètres d'engrènement"""
        if not isinstance(other, HelicalGear):
            raise ValueError("Un engrenage hélicoïdal doit s'engrener avec un autre engrenage hélicoïdal")
        
        # Vérifier que les angles d'hélice sont opposés
        if abs(self.params.helix_angle + other.params.helix_angle) > 0.1:
            raise ValueError("Les angles d'hélice doivent être opposés pour l'engrènement")
        
        # Distance entre centres
        center_distance = GearMath.center_distance(self, other)
        
        # Rapport de contact total (transverse + overlap)
        transverse_ratio = GearMath.contact_ratio_base_path(
            self, other, self.params.pressure_angle
        )
        overlap_ratio = self.params.face_width * math.tan(
            math.radians(self.params.helix_angle)
        ) / (math.pi * self.params.module)
        
        total_contact_ratio = transverse_ratio + overlap_ratio
        
        return center_distance, total_contact_ratio
    
    @property
    def pitch_diameter(self) -> float:
        """Diamètre primitif (utilise le module apparent)"""
        return self.transverse_module * self.params.teeth
    
    @property
    def transverse_pressure_angle(self) -> float:
        """Angle de pression apparent"""
        alpha_n = math.radians(self.params.pressure_angle)
        beta = math.radians(self.params.helix_angle)
        alpha_t = math.atan(math.tan(alpha_n) / math.cos(beta))
        return math.degrees(alpha_t)
    
    @property
    def normal_pitch(self) -> float:
        """Pas normal"""
        return GearMath.normal_pitch(self.params.module)
    
    @property
    def lead(self) -> float:
        """Pas de l'hélice"""
        if self.params.helix_angle == 0:
            return float('inf')
        return math.pi * self.pitch_diameter / math.tan(math.radians(self.params.helix_angle))
    
    @property
    def contact_ratio(self) -> float:
        """Rapport de contact total"""
        transverse_ratio = 1.4 + (self.params.teeth / 100)
        overlap_ratio = self.params.face_width * math.tan(
            math.radians(self.params.helix_angle)
        ) / (math.pi * self.params.module)
        return transverse_ratio + overlap_ratio
    
    def get_info(self) -> Dict[str, Any]:
        """Informations spécifiques aux engrenages hélicoïdaux"""
        info = super().get_info()
        info.update({
            'transverse_module': self.transverse_module,
            'axial_pitch': self.axial_pitch,
            'normal_pitch': self.normal_pitch,
            'transverse_pressure_angle': self.transverse_pressure_angle,
            'helix_angle': self.params.helix_angle,
            'lead': self.lead,
            'gear_type': 'helical'
        })
        return info