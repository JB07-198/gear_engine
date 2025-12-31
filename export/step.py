"""
Export STEP (ISO 10303) pour les engrenages
"""
from typing import List, Tuple, Optional
import numpy as np

class STEPExporter:
    """Exportateur de fichiers STEP"""
    
    def __init__(self):
        self.entities = []
        self.entity_counter = 1
    
    def _add_entity(self, entity_type: str, params: list) -> str:
        """Ajouter une entité STEP"""
        param_str = ','.join(str(p) for p in params)
        entity = f"#{self.entity_counter} = {entity_type}({param_str});"
        self.entities.append(entity)
        self.entity_counter += 1
        return f"#{self.entity_counter - 1}"
    
    def export_gear(self, gear, filename: str = "gear.step"):
        """Exporter un engrenage en STEP"""
        # En-tête STEP
        header = self._create_header()
        
        # Données géométriques
        data_section = self._create_gear_geometry(gear)
        
        # Écrire le fichier
        with open(filename, 'w') as f:
            f.write(header)
            f.write("DATA;\n")
            for entity in self.entities:
                f.write(entity + "\n")
            f.write("ENDSEC;\n")
            f.write("END-ISO-10303-21;\n")
    
    def _create_header(self) -> str:
        """Créer l'en-tête STEP"""
        return """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Gear Model'),'2;1');
FILE_NAME('gear_model','2024-01-01',('Engineer'),('Company'),'','','');
FILE_SCHEMA(('CONFIG_CONTROL_DESIGN'));
ENDSEC;
"""
    
    def _create_gear_geometry(self, gear) -> list:
        """Créer la géométrie STEP pour un engrenage"""
        # Points pour le cercle de base
        center = self._add_entity('CARTESIAN_POINT', ['', (0.0, 0.0, 0.0)])
        axis = self._add_entity('DIRECTION', ['', (0.0, 0.0, 1.0)])
        dir_x = self._add_entity('DIRECTION', ['', (1.0, 0.0, 0.0)])
        dir_y = self._add_entity('DIRECTION', ['', (0.0, 1.0, 0.0)])
        
        # Système de coordonnées
        axis_placement = self._add_entity('AXIS2_PLACEMENT_3D', 
                                         ['', center, axis, dir_x])
        
        # Cercle primitif
        circle = self._add_entity('CIRCLE', 
                                 ['', axis_placement, gear.pitch_diameter / 2])
        
        # Extrusion pour créer le solide
        if hasattr(gear, 'params') and hasattr(gear.params, 'face_width'):
            height = gear.params.face_width
        else:
            height = 10.0
        
        extruded_solid = self._add_entity('EXTRUDED_AREA_SOLID', 
                                         ['', circle, axis, height])
        
        return [extruded_solid]
    
    def export_mesh_pair(self, gear1, gear2, filename: str = "mesh_pair.step"):
        """Exporter une paire d'engrenages en STEP"""
        # Distancer les engrenages
        center_distance = (gear1.pitch_diameter + gear2.pitch_diameter) / 2
        
        # TODO: Implémenter la génération complète de la paire
        print(f"Export de la paire d'engrenages vers {filename}")
        print(f"Distance entre centres: {center_distance:.2f} mm")
        
        self.export_gear(gear1, "gear1_temp.step")
        self.export_gear(gear2, "gear2_temp.step")