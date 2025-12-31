"""
Export STL pour impression 3D
"""
import struct
import numpy as np
from typing import List, Tuple

class STLExporter:
    """Exportateur de fichiers STL (binaire)"""
    
    @staticmethod
    def write_binary_stl(faces: List[Tuple], filename: str):
        """
        Écrire un fichier STL binaire
        
        Args:
            faces: Liste de faces, chaque face est un tuple de 3 points (9 floats)
            filename: Nom du fichier de sortie
        """
        with open(filename, 'wb') as f:
            # En-tête (80 bytes)
            header = b'Binary STL - Gear Model' + b' ' * (80 - 23)
            f.write(header)
            
            # Nombre de faces (4 bytes, little endian)
            f.write(struct.pack('<I', len(faces)))
            
            # Écrire chaque face
            for face in faces:
                # Normale (calculée à partir des points)
                p1, p2, p3 = face
                normal = STLExporter._calculate_normal(p1, p2, p3)
                
                # Écrire la normale
                f.write(struct.pack('<3f', *normal))
                
                # Écrire les 3 vertices
                for vertex in [p1, p2, p3]:
                    f.write(struct.pack('<3f', *vertex))
                
                # Attribut byte count (2 bytes, généralement 0)
                f.write(struct.pack('<H', 0))
    
    @staticmethod
    def _calculate_normal(p1: Tuple, p2: Tuple, p3: Tuple) -> Tuple:
        """Calculer la normale d'une face"""
        v1 = np.array(p2) - np.array(p1)
        v2 = np.array(p3) - np.array(p1)
        normal = np.cross(v1, v2)
        norm = np.linalg.norm(normal)
        if norm > 0:
            normal = normal / norm
        return tuple(normal)
    
    @staticmethod
    def gear_to_faces(gear, resolution: int = 32) -> List[Tuple]:
        """
        Convertir un engrenage en faces STL
        
        Args:
            gear: Objet engrenage
            resolution: Résolution angulaire
            
        Returns:
            Liste de faces pour l'STL
        """
        faces = []
        
        # Générer les points du profil
        if hasattr(gear, 'get_tooth_points'):
            tooth_points = gear.get_tooth_points(resolution)
        else:
            # Profil par défaut (cercle)
            tooth_points = []
            for i in range(resolution):
                angle = 2 * np.pi * i / resolution
                x = gear.pitch_diameter / 2 * np.cos(angle)
                y = gear.pitch_diameter / 2 * np.sin(angle)
                tooth_points.append((x, y, 0))
        
        # Hauteur de l'engrenage
        if hasattr(gear.params, 'face_width'):
            height = gear.params.face_width
        else:
            height = 10.0
        
        # Créer les faces latérales
        for i in range(len(tooth_points)):
            p1 = tooth_points[i]
            p2 = tooth_points[(i + 1) % len(tooth_points)]
            
            # Face basse
            p1_low = (p1[0], p1[1], 0)
            p2_low = (p2[0], p2[1], 0)
            center_low = (0, 0, 0)
            faces.append((p1_low, p2_low, center_low))
            
            # Face haute
            p1_high = (p1[0], p1[1], height)
            p2_high = (p2[0], p2[1], height)
            center_high = (0, 0, height)
            faces.append((p2_high, p1_high, center_high))
            
            # Face latérale
            faces.append((p1_low, p1_high, p2_low))
            faces.append((p2_low, p1_high, p2_high))
        
        return faces
    
    @staticmethod
    def export_gear(gear, filename: str = "gear.stl", resolution: int = 64):
        """Exporter un engrenage en STL"""
        faces = STLExporter.gear_to_faces(gear, resolution)
        STLExporter.write_binary_stl(faces, filename)
        print(f"Engrenage exporté vers {filename} ({len(faces)} faces)")