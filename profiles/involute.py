import math
from typing import List, Tuple
import numpy as np

class InvoluteProfile:
    """Profil en développante de cercle (norme ISO)"""
    
    def __init__(self, pressure_angle: float = 20.0):
        self.pressure_angle = pressure_angle
        self.alpha_rad = math.radians(pressure_angle)
    
    def generate_points(self, base_radius: float, 
                       start_angle: float = 0,
                       end_angle: float = 60,
                       num_points: int = 100) -> List[Tuple[float, float]]:
        """
        Générer des points de la développante
        
        Args:
            base_radius: Rayon de base
            start_angle: Angle de départ (degrés)
            end_angle: Angle de fin (degrés)
            num_points: Nombre de points
            
        Returns:
            Liste de points (x, y)
        """
        points = []
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        for t in np.linspace(start_rad, end_rad, num_points):
            x = base_radius * (math.cos(t) + t * math.sin(t))
            y = base_radius * (math.sin(t) - t * math.cos(t))
            points.append((x, y))
        
        return points
    
    def pressure_angle_at_radius(self, base_radius: float, 
                                radius: float) -> float:
        """Calculer l'angle de pression à un rayon donné"""
        if radius <= base_radius:
            return 0
        alpha = math.acos(base_radius / radius)
        return math.degrees(alpha)
    
    def thickness_at_radius(self, base_radius: float, 
                           pitch_radius: float,
                           thickness_at_pitch: float,
                           radius: float) -> float:
        """
        Épaisseur de la dent à un rayon donné
        
        Args:
            base_radius: Rayon de base
            pitch_radius: Rayon primitif
            thickness_at_pitch: Épaisseur au primitif
            radius: Rayon où calculer l'épaisseur
            
        Returns:
            Épaisseur de la dent au rayon spécifié
        """
        if radius < base_radius:
            return 0
        
        # Angle d'involute au primitif
        inv_alpha = math.tan(self.alpha_rad) - self.alpha_rad
        
        # Angle d'involute au rayon spécifié
        alpha_r = math.acos(base_radius / radius)
        inv_alpha_r = math.tan(alpha_r) - alpha_r
        
        # Épaisseur au rayon spécifié
        thickness = radius * (thickness_at_pitch / pitch_radius + 
                             2 * (inv_alpha - inv_alpha_r))
        
        return thickness
    
    @staticmethod
    def contact_point(pitch_point1: Tuple[float, float],
                     pitch_point2: Tuple[float, float],
                     line_of_action: float) -> Tuple[float, float]:
        """
        Point de contact sur la ligne d'action
        """
        # Simplification: point au milieu
        x = (pitch_point1[0] + pitch_point2[0]) / 2
        y = (pitch_point1[1] + pitch_point2[1]) / 2
        
        return (x, y)