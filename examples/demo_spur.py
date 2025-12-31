"""
Démonstration d'engrenage droit
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.gear_factory import GearFactory
from core.base_gear import GearParams
from gears.spur import SpurGear
from gears.helical import HelicalGear

# Enregistrer les types
GearFactory.register_gear('spur', SpurGear)
GearFactory.register_gear('helical', HelicalGear)

def demo_spur_gear():
    """Démonstration d'un engrenage droit simple"""
    print("="*60)
    print("DÉMONSTRATION: ENGRENAGE DROIT")
    print("="*60)
    
    # Créer un engrenage droit
    params = GearParams(
        name="PignonDemo",
        module=2.0,
        teeth=20,
        pressure_angle=20.0,
        face_width=15.0
    )
    
    gear = SpurGear(params)
    
    # Afficher les informations
    info = gear.get_info()
    print("\nInformations de l'engrenage:")
    print("-"*40)
    for key, value in info.items():
        if isinstance(value, float):
            print(f"{key:20}: {value:.3f}")
        else:
            print(f"{key:20}: {value}")
    
    # Afficher les dimensions principales
    print("\nDimensions principales:")
    print("-"*40)
    print(f"Diamètre primitif:  {gear.pitch_diameter:.2f} mm")
    print(f"Diamètre extérieur: {gear.outside_diameter:.2f} mm")
    print(f"Diamètre de pied:   {gear.root_diameter:.2f} mm")
    print(f"Hauteur de dent:    {gear.addendum + gear.dedendum:.2f} mm")
    
    return gear

def demo_helical_gear():
    """Démonstration d'un engrenage hélicoïdal"""
    print("\n" + "="*60)
    print("DÉMONSTRATION: ENGRENAGE HÉLICOÏDAL")
    print("="*60)
    
    # Créer un engrenage hélicoïdal
    params = GearParams(
        name="HelicalDemo",
        module=2.0,
        teeth=30,
        pressure_angle=20.0,
        helix_angle=15.0,
        face_width=20.0
    )
    
    gear = HelicalGear(params)
    
    # Afficher les informations spécifiques
    info = gear.get_info()
    print("\nInformations spécifiques hélicoïdales:")
    print("-"*40)
    specific_keys = ['transverse_module', 'axial_pitch', 'lead', 
                     'helix_angle', 'transverse_pressure_angle']
    
    for key in specific_keys:
        if key in info:
            value = info[key]
            if isinstance(value, float):
                print(f"{key:30}: {value:.3f}")
            else:
                print(f"{key:30}: {value}")
    
    return gear

def demo_mesh_pair():
    """Démonstration d'une paire d'engrenages"""
    print("\n" + "="*60)
    print("DÉMONSTRATION: ENGRÈNEMENT")
    print("="*60)
    
    # Créer deux engrenages droits
    params1 = GearParams(
        name="Pignon",
        module=2.0,
        teeth=20,
        pressure_angle=20.0
    )
    
    params2 = GearParams(
        name="Roue",
        module=2.0,
        teeth=40,
        pressure_angle=20.0
    )
    
    gear1 = SpurGear(params1)
    gear2 = SpurGear(params2)
    
    # Analyser l'engrènement
    try:
        center_distance, contact_ratio = gear1.mesh_with(gear2)
        
        print(f"\nEngrènement: {gear1.params.name} avec {gear2.params.name}")
        print("-"*40)
        print(f"Distance entre centres: {center_distance:.2f} mm")
        print(f"Rapport de contact:     {contact_ratio:.2f}")
        print(f"Rapport de transmission: {gear2.params.teeth / gear1.params.teeth:.2f}")
        
        if contact_ratio >= 1.2:
            print("✓ Bon engrènement (rapport de contact ≥ 1.2)")
        elif contact_ratio >= 1.0:
            print("⚠️  Engrènement acceptable (rapport de contact ≥ 1.0)")
        else:
            print("✗ Mauvaise continuité d'engrènement")
            
    except Exception as e:
        print(f"Erreur d'engrènement: {e}")

def demo_gear_factory():
    """Démonstration de la fabrique d'engrenages"""
    print("\n" + "="*60)
    print("DÉMONSTRATION: FABRIQUE D'ENGRENAGES")
    print("="*60)
    
    # Créer différents types d'engrenages via la fabrique
    gear_configs = [
        {'type': 'spur', 'name': 'Spur1', 'module': 2.0, 'teeth': 25},
        {'type': 'helical', 'name': 'Helical1', 'module': 2.0, 'teeth': 30, 'helix_angle': 20.0},
    ]
    
    for config in gear_configs:
        params = GearParams(
            name=config['name'],
            module=config['module'],
            teeth=config['teeth'],
            helix_angle=config.get('helix_angle', 0.0)
        )
        
        gear = GearFactory.create_gear(config['type'], params)
        print(f"\n{gear.__class__.__name__}: {gear.params.name}")
        print(f"  Diamètre primitif: {gear.pitch_diameter:.1f} mm")
        print(f"  Diamètre extérieur: {gear.outside_diameter:.1f} mm")

def main():
    """Fonction principale de démonstration"""
    print("\n" + "="*60)
    print("GEAR ENGINE - SYSTÈME DE CONCEPTION D'ENGRENAGES")
    print("="*60)
    
    # Exécuter les démonstrations
    demo_spur_gear()
    demo_helical_gear()
    demo_mesh_pair()
    demo_gear_factory()
    
    print("\n" + "="*60)
    print("DÉMONSTRATION TERMINÉE")
    print("="*60)

if __name__ == "__main__":
    main()