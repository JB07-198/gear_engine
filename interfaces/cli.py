"""
Interface en ligne de commande
"""
import argparse
import json
from core.gear_factory import GearFactory
from core.base_gear import GearParams
from gears.spur import SpurGear
from gears.helical import HelicalGear
from gears.bevel import BevelGear
from gears.worm import WormGear
from gears.rack import RackGear
from gears.internal import InternalGear
from export.step import STEPExporter
from export.stl import STLExporter

# Enregistrer les types d'engrenages
GearFactory.register_gear('spur', SpurGear)
GearFactory.register_gear('helical', HelicalGear)
GearFactory.register_gear('bevel', BevelGear)
GearFactory.register_gear('worm', WormGear)
GearFactory.register_gear('rack', RackGear)
GearFactory.register_gear('internal', InternalGear)


class GearCLI:
    """Interface CLI pour le système d'engrenages"""

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Créer le parseur d'arguments"""
        parser = argparse.ArgumentParser(
            description="Système de conception d'engrenages",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        subparsers = parser.add_subparsers(dest='command', help='Commandes')

        # Commande: créer un engrenage
        create_parser = subparsers.add_parser('create', help='Créer un engrenage')
        create_parser.add_argument('--config', type=str,
                                   help='Fichier JSON pour créer l\'engrenage')
        create_parser.add_argument('--type', type=str, default='spur',
                                   choices=GearFactory.get_available_types(),
                                   help='Type d\'engrenage')
        create_parser.add_argument('--name', type=str, default='Gear1',
                                   help='Nom de l\'engrenage')
        create_parser.add_argument('--module', type=float,
                                   help='Module (mm)')
        create_parser.add_argument('--teeth', type=int,
                                   help='Nombre de dents')
        create_parser.add_argument('--pressure-angle', type=float, default=20.0,
                                   help='Angle de pression (degrés)')
        create_parser.add_argument('--helix-angle', type=float, default=0.0,
                                   help='Angle d\'hélice (degrés)')
        create_parser.add_argument('--face-width', type=float, default=10.0,
                                   help='Largeur de face (mm)')
        create_parser.add_argument('--pitch-angle', type=float, default=None,
                                   help='Angle de pas (degrés)')
        create_parser.add_argument('--shaft-angle', type=float, default=90,
                                   help='Angle d\'axe (degrés)')
        create_parser.add_argument('--leads', type=int, default=None,
                                   help='Nombre de filetages (vis sans fin)')

        # Commande: analyser
        analyze_parser = subparsers.add_parser('analyze', help='Analyser un engrenage')
        analyze_parser.add_argument('--config', type=str, required=True,
                                    help='Fichier de configuration JSON')

        # Commande: exporter
        export_parser = subparsers.add_parser('export', help='Exporter un engrenage')
        export_parser.add_argument('--config', type=str, required=True,
                                   help='Fichier de configuration JSON')
        export_parser.add_argument('--format', type=str, default='step',
                                   choices=['step', 'stl'],
                                   help='Format d\'export')
        export_parser.add_argument('--output', type=str,
                                   help='Fichier de sortie')

        # Commande: liste
        subparsers.add_parser('list', help='Lister les types d\'engrenages')

        # Commande: mesh
        mesh_parser = subparsers.add_parser('mesh', help='Analyser un engrènement')
        mesh_parser.add_argument('--gear1', type=str, required=True,
                                 help='Configuration engrenage 1 (JSON)')
        mesh_parser.add_argument('--gear2', type=str, required=True,
                                 help='Configuration engrenage 2 (JSON)')

        return parser

    def run(self):
        """Exécuter l'interface CLI"""
        args = self.parser.parse_args()

        if args.command == 'create':
            self._handle_create(args)
        elif args.command == 'analyze':
            self._handle_analyze(args)
        elif args.command == 'export':
            self._handle_export(args)
        elif args.command == 'list':
            self._handle_list()
        elif args.command == 'mesh':
            self._handle_mesh(args)
        else:
            self.parser.print_help()

    def _handle_create(self, args):
        """Gérer la création d'engrenage"""
        try:
            if args.config:
                # Lecture JSON
                with open(args.config, 'r') as f:
                    config = json.load(f)
                gear = GearFactory.from_dict(config)
            else:
                # Vérifier que module et teeth sont fournis
                if args.module is None or args.teeth is None:
                    print("Erreur: --module et --teeth sont obligatoires si --config n'est pas fourni.")
                    return

                # Préparer les paramètres de base
                params_dict = {
                    'name': args.name,
                    'module': args.module,
                    'teeth': args.teeth,
                    'pressure_angle': args.pressure_angle,
                    'helix_angle': args.helix_angle,
                    'face_width': args.face_width,
                }
                
                # Ajouter les paramètres optionnels pour engrenages coniques
                if args.pitch_angle is not None:
                    params_dict['pitch_angle'] = args.pitch_angle
                if hasattr(args, 'shaft_angle') and args.shaft_angle is not None:
                    params_dict['shaft_angle'] = args.shaft_angle
                
                # Ajouter les paramètres optionnels pour vis sans fin
                if hasattr(args, 'leads') and args.leads is not None:
                    params_dict['leads'] = args.leads
                
                params = GearParams(**params_dict)
                gear = GearFactory.create_gear(args.type, params)

            info = gear.get_info()

            print("\n" + "="*50)
            print(f"ENGRENAGE CRÉÉ: {info['name']}")
            print("="*50)

            for key, value in info.items():
                if isinstance(value, float):
                    print(f"{key:25}: {value:.3f}")
                else:
                    print(f"{key:25}: {value}")

            print("\nParamètres calculés:")
            print(f"  Diamètre primitif:   {gear.pitch_diameter:.2f} mm")
            print(f"  Diamètre extérieur:  {gear.outside_diameter:.2f} mm")
            print(f"  Diamètre de pied:    {gear.root_diameter:.2f} mm")

        except Exception as e:
            print(f"Erreur: {e}")

    def _handle_analyze(self, args):
        """Analyser un engrenage à partir d'un fichier de configuration"""
        with open(args.config, 'r') as f:
            config = json.load(f)

        gear = GearFactory.from_dict(config)
        info = gear.get_info()

        print("\nANALYSE D'ENGRENAGE")
        print("="*50)

        for key, value in info.items():
            if isinstance(value, float):
                print(f"{key:30}: {value:.3f}")
            else:
                print(f"{key:30}: {value}")

    def _handle_export(self, args):
        """Exporter un engrenage"""
        with open(args.config, 'r') as f:
            config = json.load(f)

        gear = GearFactory.from_dict(config)

        if args.output:
            output_file = args.output
        else:
            output_file = f"{gear.params.name.lower()}.{args.format}"

        if args.format == 'step':
            exporter = STEPExporter()
            exporter.export_gear(gear, output_file)
        elif args.format == 'stl':
            STLExporter.export_gear(gear, output_file)

        print(f"Engrenage exporté vers: {output_file}")

    def _handle_list(self):
        """Lister les types d'engrenages disponibles"""
        types = GearFactory.get_available_types()

        print("\nTYPES D'ENGRENAGES DISPONIBLES")
        print("="*50)

        for i, gear_type in enumerate(types, 1):
            print(f"{i:2}. {gear_type}")

        print(f"\nTotal: {len(types)} types")

    def _handle_mesh(self, args):
        """Analyser un engrènement"""
        with open(args.gear1, 'r') as f:
            config1 = json.load(f)

        with open(args.gear2, 'r') as f:
            config2 = json.load(f)

        gear1 = GearFactory.from_dict(config1)
        gear2 = GearFactory.from_dict(config2)

        try:
            center_distance, contact_ratio = gear1.mesh_with(gear2)

            print("\nANALYSE D'ENGRÈNEMENT")
            print("="*50)
            print(f"Engrenage 1: {gear1.params.name}")
            print(f"Engrenage 2: {gear2.params.name}")
            print(f"Distance entre centres: {center_distance:.2f} mm")
            print(f"Rapport de contact: {contact_ratio:.2f}")

            if contact_ratio < 1.0:
                print("⚠️  ATTENTION: Rapport de contact < 1.0 (engrènement discontinu)")
            elif contact_ratio < 1.2:
                print("ℹ️   Rapport de contact acceptable")
            else:
                print("✓ Rapport de contact bon")

        except Exception as e:
            print(f"Erreur d'engrènement: {e}")


def main():
    """Point d'entrée principal"""
    cli = GearCLI()
    cli.run()


if __name__ == "__main__":
    main()
