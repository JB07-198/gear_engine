import math
from typing import Tuple, Optional

class GearMath:
    """Utilitaires mathématiques pour les engrenages (normes ISO)"""
    
    @staticmethod
    def base_diameter(pitch_diameter: float, pressure_angle: float) -> float:
        """Diamètre de base"""
        return pitch_diameter * math.cos(math.radians(pressure_angle))
    
    @staticmethod
    def transverse_module(normal_module: float, helix_angle: float) -> float:
        """Module apparent"""
        if helix_angle == 0:
            return normal_module
        return normal_module / math.cos(math.radians(helix_angle))
    
    @staticmethod
    def axial_pitch(module: float, helix_angle: float) -> float:
        """Pas axial"""
        if helix_angle == 0:
            return float('inf')
        return math.pi * module / math.tan(math.radians(helix_angle))
    
    @staticmethod
    def normal_pitch(module: float) -> float:
        """Pas normal"""
        return math.pi * module
    
    @staticmethod
    def center_distance(gear1, gear2) -> float:
        """Distance entre centres"""
        return (gear1.pitch_diameter + gear2.pitch_diameter) / 2
    
    @staticmethod
    def contact_ratio_base_path(gear1, gear2, 
                                pressure_angle: float = 20.0) -> float:
        """Calcul du rapport de contact (approche ISO)"""
        # Rayons de base
        rb1 = gear1.pitch_diameter / 2 * math.cos(math.radians(pressure_angle))
        rb2 = gear2.pitch_diameter / 2 * math.cos(math.radians(pressure_angle))
        
        # Rayons de tête
        ra1 = gear1.outside_diameter / 2
        ra2 = gear2.outside_diameter / 2
        
        # Distance entre centres
        a = (gear1.pitch_diameter + gear2.pitch_diameter) / 2
        
        # Longueur d'action
        g_alpha = (math.sqrt(ra1**2 - rb1**2) + 
                   math.sqrt(ra2**2 - rb2**2) - 
                   a * math.sin(math.radians(pressure_angle)))
        
        # Pas de base
        p_b = math.pi * gear1.params.module * math.cos(math.radians(pressure_angle))
        
        return g_alpha / p_b if p_b != 0 else 0
    
    @staticmethod
    def profile_shift_coefficient(min_teeth: int = 17, 
                                  pressure_angle: float = 20.0) -> float:
        """Coefficient de déport pour éviter l'interférence"""
        if min_teeth >= 17:
            return 0
        # Formule simplifiée ISO
        return (17 - min_teeth) / 17
    
    @staticmethod
    def bending_stress(torque: float, module: float, face_width: float, 
                       teeth: int, factor: float = 1.0) -> float:
        """Contrainte de flexion simplifiée (Lewis)"""
        # Force tangentielle
        Ft = 2 * torque / (module * teeth)
        # Contrainte
        return factor * Ft / (face_width * module)