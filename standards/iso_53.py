"""
Norme ISO 53:1998 - Profil de référence pour engrenages cylindriques
"""
import math

class ISO53:
    """Implémentation de la norme ISO 53"""
    
    # Coefficients pour hauteur de dent (ISO 53:1998)
    HA_STAR = 1.0      # Coefficient de hauteur de tête
    HF_STAR = 1.25     # Coefficient de hauteur de pied
    C_STAR = 0.25      # Coefficient de jeu
    
    # Rayons d'arrondi (Table 1 ISO 53)
    RADIUS_COEFFICIENTS = {
        'standard': 0.38,
        'full_fillet': 0.3,
        'reduced': 0.25
    }
    
    @classmethod
    def addendum(cls, module: float) -> float:
        """Hauteur de tête selon ISO 53"""
        return cls.HA_STAR * module
    
    @classmethod
    def dedendum(cls, module: float, profile: str = 'standard') -> float:
        """Hauteur de pied selon ISO 53"""
        return cls.HF_STAR * module
    
    @classmethod
    def tip_radius(cls, module: float, profile: str = 'standard') -> float:
        """Rayon d'arrondi de tête"""
        coeff = cls.RADIUS_COEFFICIENTS.get(profile, 0.38)
        return coeff * module
    
    @classmethod
    def root_radius(cls, module: float, profile: str = 'standard') -> float:
        """Rayon d'arrondi de pied"""
        coeff = cls.RADIUS_COEFFICIENTS.get(profile, 0.38)
        return coeff * module
    
    @classmethod
    def clearance(cls, module: float) -> float:
        """Jeu au fond de dent"""
        return cls.C_STAR * module
    
    @classmethod
    def basic_rack_profile(cls, module: float, pressure_angle: float = 20.0):
        """Profil de crémaillère de base selon ISO 53"""
        alpha = math.radians(pressure_angle)
        
        profile = {
            'module': module,
            'pressure_angle': pressure_angle,
            'addendum': cls.addendum(module),
            'dedendum': cls.dedendum(module),
            'tip_radius': cls.tip_radius(module),
            'root_radius': cls.root_radius(module),
            'clearance': cls.clearance(module),
            'tooth_thickness': math.pi * module / 2,
            'space_width': math.pi * module / 2
        }
        
        return profile