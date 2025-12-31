from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
import math

@dataclass
class GearParams:
    """Paramètres d'engrenage de base"""
    name: str
    module: float
    teeth: int
    pressure_angle: float = 20.0
    helix_angle: float = 0.0
    profile_shift: float = 0.0
    backlash: float = 0.0
    face_width: float = 10.0
    material: str = "steel"
    pitch_angle: Optional[float] = None  # Pour engrenages coniques
    shaft_angle: Optional[float] = None  # Pour engrenages coniques
    mate_teeth: Optional[int] = None  # Nombre de dents de l'engrenage conjugué
    leads: Optional[int] = None  # Nombre de filetages pour vis sans fin
    
    def validate(self):
        """Validation des paramètres de base"""
        if self.module <= 0:
            raise ValueError(f"Module doit être > 0, got {self.module}")
        if self.teeth < 1:
            raise ValueError(f"Nombre de dents doit être >= 1, got {self.teeth}")
        if not (14 <= self.pressure_angle <= 25):
            raise ValueError(f"Angle de pression doit être entre 14° et 25°, got {self.pressure_angle}")

class Gear(ABC):
    """Classe abstraite pour tous les types d'engrenages"""
    
    def __init__(self, params: GearParams):
        self.params = params
        self.params.validate()
        self._calculate_geometry()
    
    @abstractmethod
    def _calculate_geometry(self):
        """Calculer la géométrie spécifique"""
        pass
    
    @abstractmethod
    def mesh_with(self, other: 'Gear') -> Tuple[float, float]:
        """Calculer les paramètres d'engrènement"""
        pass
    
    @property
    def pitch_diameter(self) -> float:
        """Diamètre primitif"""
        return self.params.module * self.params.teeth
    
    @property
    def addendum(self) -> float:
        """Hauteur de tête"""
        return self.params.module
    
    @property
    def dedendum(self) -> float:
        """Hauteur de pied"""
        return 1.25 * self.params.module
    
    @property
    def outside_diameter(self) -> float:
        """Diamètre extérieur"""
        return self.pitch_diameter + 2 * self.addendum
    
    @property
    def root_diameter(self) -> float:
        """Diamètre de pied"""
        return self.pitch_diameter - 2 * self.dedendum
    
    @property
    def contact_ratio(self) -> float:
        """Rapport de contact"""
        raise NotImplementedError
    
    def get_info(self) -> Dict[str, Any]:
        """Retourne les informations de l'engrenage"""
        return {
            'name': self.params.name,
            'type': self.__class__.__name__,
            'module': self.params.module,
            'teeth': self.params.teeth,
            'pitch_diameter': self.pitch_diameter,
            'outside_diameter': self.outside_diameter,
            'root_diameter': self.root_diameter,
            'addendum': self.addendum,
            'dedendum': self.dedendum,
            'face_width': self.params.face_width
        }
    
    def __str__(self) -> str:
        info = self.get_info()
        return (f"{info['type']} '{info['name']}': "
                f"m={info['module']}, z={info['teeth']}, "
                f"d={info['pitch_diameter']:.2f}mm")