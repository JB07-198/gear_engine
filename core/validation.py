from typing import Dict, Any, List, Tuple
from .base_gear import Gear, GearParams

class GearValidator:
    """Validation des engrenages et des paires"""
    
    @staticmethod
    def validate_gear_params(params: GearParams) -> List[str]:
        """Valider les paramètres d'un engrenage"""
        errors = []
        
        # Vérification module
        if params.module <= 0:
            errors.append("Le module doit être positif")
        
        # Vérification nombre de dents
        if params.teeth < 1:
            errors.append("Le nombre de dents doit être >= 1")
        elif params.teeth < 12:
            errors.append(f"Attention: {params.teeth} dents peut causer de l'interférence")
        
        # Vérification angle de pression
        if not (14 <= params.pressure_angle <= 25):
            errors.append("L'angle de pression doit être entre 14° et 25°")
        
        # Vérification angle d'hélice
        if abs(params.helix_angle) > 45:
            errors.append("L'angle d'hélice doit être entre -45° et 45°")
        
        return errors
    
    @staticmethod
    def validate_mesh_pair(gear1: Gear, gear2: Gear) -> List[str]:
        """Valider une paire d'engrenages"""
        errors = []
        
        # Vérification module
        if abs(gear1.params.module - gear2.params.module) > 0.001:
            errors.append("Les modules doivent être identiques")
        
        # Vérification angle de pression
        if abs(gear1.params.pressure_angle - gear2.params.pressure_angle) > 0.1:
            errors.append("Les angles de pression doivent être identiques")
        
        # Vérification pour engrenages hélicoïdaux
        if (gear1.params.helix_angle != 0 or gear2.params.helix_angle != 0):
            if abs(gear1.params.helix_angle + gear2.params.helix_angle) > 0.1:
                errors.append("Les angles d'hélice doivent être opposés pour un engrènement correct")
        
        return errors
    
    @staticmethod
    def check_interference(gear: Gear) -> Tuple[bool, str]:
        """Vérifier l'interférence"""
        if gear.params.teeth < 17 and gear.params.profile_shift == 0:
            return (True, 
                   f"Interférence possible avec {gear.params.teeth} dents. "
                   f"Utiliser un déport de profil.")
        return (False, "Pas d'interférence détectée")
    
    @staticmethod
    def check_undercut(gear: Gear) -> bool:
        """Vérifier le sous-dépouille"""
        min_teeth_no_undercut = {
            14.5: 32,
            20: 18,
            25: 12
        }
        min_teeth = min_teeth_no_undercut.get(
            round(gear.params.pressure_angle), 17
        )
        return gear.params.teeth < min_teeth