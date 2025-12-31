# profiles/cycloidal.py - Version corrigée
import math
from typing import List, Tuple
import numpy as np

class CycloidalProfile:
    """Profil cycloïdal (pour engrenages spéciaux)"""
    
    def __init__(self, rolling_circle_ratio: float = 0.5):
        self.rolling_ratio = rolling_circle_ratio
    
    def generate_points(self, pitch_radius: float,
                       rolling_radius: float = None,
                       num_points: int = 100) -> List[Tuple[float, float]]:
        """
        Générer des points de profil cycloïdal
        """
        if rolling_radius is None:
            rolling_radius = pitch_radius * self.rolling_ratio
        
        points = []
        
        for theta in np.linspace(0, 2 * math.pi, num_points):
            # Coordonnées du point sur la cycloïde
            x = (pitch_radius + rolling_radius) * math.cos(theta) - \
                rolling_radius * math.cos((pitch_radius + rolling_radius) * theta / rolling_radius)
            y = (pitch_radius + rolling_radius) * math.sin(theta) - \
                rolling_radius * math.sin((pitch_radius + rolling_radius) * theta / rolling_radius)
            
            points.append((x, y))
        
        return points
    
    def curvature_radius(self, pitch_radius: float,
                        rolling_radius: float,
                        angle: float) -> float:
        """
        Rayon de courbure du profil
        """
        return 4 * rolling_radius * abs(math.sin(angle / 2))