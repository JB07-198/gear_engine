"""
Norme ISO 21771:2007 - Engrenages cylindriques à denture hélicoïdale
"""
import math

class ISO21771:
    """Implémentation de la norme ISO 21771 pour engrenages hélicoïdaux"""
    
    @staticmethod
    def transverse_pressure_angle(normal_pressure_angle: float, 
                                  helix_angle: float) -> float:
        """Angle de pression apparent (Éq. 1)"""
        alpha_n = math.radians(normal_pressure_angle)
        beta = math.radians(helix_angle)
        alpha_t = math.atan(math.tan(alpha_n) / math.cos(beta))
        return math.degrees(alpha_t)
    
    @staticmethod
    def transverse_module(normal_module: float, helix_angle: float) -> float:
        """Module apparent (Éq. 2)"""
        beta = math.radians(helix_angle)
        return normal_module / math.cos(beta)
    
    @staticmethod
    def axial_pitch(normal_module: float, helix_angle: float) -> float:
        """Pas axial (Éq. 3)"""
        beta = math.radians(helix_angle)
        return math.pi * normal_module / math.tan(beta)
    
    @staticmethod
    def overlap_ratio(face_width: float, helix_angle: float, 
                      normal_module: float) -> float:
        """Rapport de recouvrement (Éq. 4)"""
        beta = math.radians(helix_angle)
        epsilon_beta = face_width * math.tan(beta) / (math.pi * normal_module)
        return epsilon_beta
    
    @staticmethod
    def total_contact_ratio(transverse_contact_ratio: float,
                            overlap_ratio: float) -> float:
        """Rapport de contact total (Éq. 5)"""
        return transverse_contact_ratio + overlap_ratio
    
    @staticmethod
    def minimum_face_width(helix_angle: float, normal_module: float,
                           desired_overlap: float = 1.0) -> float:
        """Largeur de face minimale pour un recouvrement donné"""
        beta = math.radians(helix_angle)
        return desired_overlap * math.pi * normal_module / math.tan(beta)
    
    @staticmethod
    def equivalent_spur_gear_teeth(actual_teeth: int, 
                                   helix_angle: float) -> float:
        """Nombre de dents virtuel pour calculs de résistance"""
        beta = math.radians(helix_angle)
        return actual_teeth / (math.cos(beta) ** 3)