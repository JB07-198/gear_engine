"""
Exportateur d'engrenages avec Trimesh
"""
import numpy as np
import trimesh
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.base_gear import GearParams
from gears.spur import SpurGear

def create_gear_mesh(gear, resolution=64):
    """Créer un maillage 3D d'engrenage avec Trimesh"""
    gear_name = gear.params.name
    print(f"Création du maillage pour {gear_name}...")
    
    # Tous les paramètres via params ou calculs
    num_teeth = gear.params.teeth
    pitch_radius = gear.pitch_diameter / 2
    outer_radius = gear.outside_diameter / 2
    root_radius = gear.root_diameter / 2
    height = gear.params.face_width
    
    print(f"  Dents: {num_teeth}")
    print(f"  Rayon primitif: {pitch_radius:.2f} mm")
    print(f"  Rayon extérieur: {outer_radius:.2f} mm")
    print(f"  Rayon de pied: {root_radius:.2f} mm")
    print(f"  Hauteur: {height:.2f} mm")
    
    # Points par dent
    points_per_tooth = max(6, resolution // num_teeth)
    total_points = num_teeth * points_per_tooth
    
    print(f"  Résolution: {total_points} points ({points_per_tooth} par dent)")
    
    # Générer les vertices
    vertices = []
    
    for i in range(total_points):
        angle = 2 * np.pi * i / total_points
        tooth_fraction = (i % points_per_tooth) / points_per_tooth
        
        # Profil de dent simplifié
        if tooth_fraction < 0.25:
            r = root_radius + (outer_radius - root_radius) * (tooth_fraction / 0.25)
        elif tooth_fraction < 0.75:
            r = outer_radius
        else:
            r = outer_radius - (outer_radius - root_radius) * ((tooth_fraction - 0.75) / 0.25)
        
        x = r * np.cos(angle)
        y = r * np.sin(angle)
        
        vertices.append([x, y, 0])
        vertices.append([x, y, height])
    
    vertices = np.array(vertices)
    vertex_count = len(vertices)
    
    # Créer les faces
    faces = []
    
    # Faces latérales
    for i in range(0, vertex_count - 2, 2):
        faces.append([i, i+2, i+1])
        faces.append([i+1, i+2, i+3])
    
    faces.append([vertex_count-2, 0, vertex_count-1])
    faces.append([vertex_count-1, 0, 1])
    
    # Face du bas
    center_bottom = len(vertices)
    vertices = np.vstack([vertices, [0, 0, 0]])
    for i in range(0, vertex_count - 2, 2):
        faces.append([center_bottom, i+2, i])
    faces.append([center_bottom, 0, vertex_count-2])
    
    # Face du haut
    center_top = len(vertices)
    vertices = np.vstack([vertices, [0, 0, height]])
    for i in range(1, vertex_count - 1, 2):
        faces.append([center_top, i, i+2])
    faces.append([center_top, vertex_count-1, 1])
    
    faces = np.array(faces)
    
    # Créer le maillage
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.fix_normals()
    
    print(f"  ✅ Maillage: {len(vertices)} sommets, {len(faces)} faces")
    
    return mesh

# ========== SCRIPT PRINCIPAL ==========

if __name__ == "__main__":
    print("=" * 70)
    print("EXPORTATEUR D'ENGRENAGES AVEC TRIMESH")
    print("=" * 70)
    print()
    
    print("Création de l'engrenage...")
    
    params = GearParams(
        name="EngrenageTest",
        module=2.5,
        teeth=24,
        pressure_angle=20.0,
        face_width=12.0
    )
    
    gear = SpurGear(params)
    
    print()
    print(f"✅ Engrenage créé: {params.name}")
    print(f"   Module: {params.module} mm")
    print(f"   Dents: {params.teeth}")
    print(f"   Ø primitif: {gear.pitch_diameter:.2f} mm")
    print(f"   Ø extérieur: {gear.outside_diameter:.2f} mm")
    print(f"   Ø pied: {gear.root_diameter:.2f} mm")
    print()
    
    print("Export STL...")
    mesh = create_gear_mesh(gear, resolution=96)
    mesh.export('gear_trimesh.stl')
    print(f"  ✅ Fichier: gear_trimesh.stl")
    
    file_size = os.path.getsize('gear_trimesh.stl') / 1024
    
    print()
    print("=" * 70)
    print("✅ EXPORT RÉUSSI !")
    print("=" * 70)
    print(f"📁 gear_trimesh.stl ({file_size:.1f} KB)")
    print(f"📊 {mesh.vertices.shape[0]} sommets, {mesh.faces.shape[0]} faces")
    print()
    print("🌐 Visualisez: https://3dviewer.net/")
    
    if os.path.exists('mon_engrenage.stl'):
        old_size = os.path.getsize('mon_engrenage.stl') / 1024
        print()
        print(f"📊 Comparaison:")
        print(f"  Ancien (cylindre): {old_size:.1f} KB")
        print(f"  Nouveau (dents):   {file_size:.1f} KB")
    
    print("=" * 70)
