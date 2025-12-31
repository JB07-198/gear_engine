from typing import Dict, Type, Any
from .base_gear import Gear, GearParams


class GearFactory:
    """Fabrique pour créer différents types d'engrenages"""

    _gear_types: Dict[str, Type[Gear]] = {}

    @classmethod
    def register_gear(cls, name: str, gear_class: Type[Gear]):
        """Enregistrer un nouveau type d'engrenage"""
        cls._gear_types[name.lower()] = gear_class

    @classmethod
    def create_gear(cls, gear_type: str, params: GearParams, **kwargs) -> Gear:
        """Créer un engrenage du type spécifié"""
        gear_type_lower = gear_type.lower()

        if gear_type_lower not in cls._gear_types:
            available = list(cls._gear_types.keys())
            raise ValueError(
                f"Type d'engrenage '{gear_type}' non supporté. "
                f"Types disponibles: {available}"
            )

        # Mettre à jour les paramètres avec les kwargs
        for key, value in kwargs.items():
            if hasattr(params, key):
                setattr(params, key, value)

        gear_class = cls._gear_types[gear_type_lower]
        return gear_class(params)

    @classmethod
    def get_available_types(cls) -> list:
        """Retourne la liste des types d'engrenages disponibles"""
        return list(cls._gear_types.keys())

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> Gear:
        """
        Créer un engrenage à partir d'un dictionnaire de configuration JSON.
        Tous les paramètres spécifiques (bevel, worm, etc.)
        sont portés par GearParams.
        """
        config = config.copy()

        gear_type = config.pop("type", "spur")
        
        # Extraire les paramètres s'ils sont dans une clé 'params'
        if 'params' in config:
            params_dict = config.pop('params')
            params_dict.update({k: v for k, v in config.items() 
                               if k not in ['type']})
        else:
            params_dict = config

        # Création des paramètres (inclut mate_teeth, shaft_angle, etc.)
        params = GearParams(**params_dict)

        return cls.create_gear(gear_type, params)

