"""
API REST pour le système d'engrenages
"""
from flask import Flask, request, jsonify
import json
from typing import Dict, Any
from core.gear_factory import GearFactory
from core.base_gear import GearParams
from gears.spur import SpurGear
from gears.helical import HelicalGear
from gears.bevel import BevelGear
from gears.worm import WormGear
from gears.rack import RackGear
from gears.internal import InternalGear

# Enregistrer les types d'engrenages
GearFactory.register_gear('spur', SpurGear)
GearFactory.register_gear('helical', HelicalGear)
GearFactory.register_gear('bevel', BevelGear)
GearFactory.register_gear('worm', WormGear)
GearFactory.register_gear('rack', RackGear)
GearFactory.register_gear('internal', InternalGear)

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de santé"""
    return jsonify({'status': 'healthy', 'service': 'gear_engine'})

@app.route('/api/gear/types', methods=['GET'])
def get_gear_types():
    """Obtenir la liste des types d'engrenages disponibles"""
    types = GearFactory.get_available_types()
    return jsonify({'types': types, 'count': len(types)})

@app.route('/api/gear/create', methods=['POST'])
def create_gear():
    """Créer un nouvel engrenage"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données JSON requises'}), 400
        
        gear_type = data.get('type', 'spur')
        params_dict = data.get('params', data)
        
        # Créer les paramètres
        params = GearParams(**params_dict)
        
        # Créer l'engrenage
        gear = GearFactory.create_gear(gear_type, params)
        
        # Retourner les informations
        info = gear.get_info()
        
        return jsonify({
            'success': True,
            'gear': info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/gear/analyze', methods=['POST'])
def analyze_gear():
    """Analyser un engrenage existant"""
    try:
        data = request.get_json()
        
        if 'gear' not in data:
            return jsonify({'error': 'Configuration d\'engrenage requise'}), 400
        
        gear = GearFactory.from_dict(data['gear'])
        info = gear.get_info()
        
        # Ajouter des analyses supplémentaires
        analysis = {
            'basic_info': info,
            'performances': {
                'bending_stress': 'N/A',
                'contact_stress': 'N/A'
            },
            'validations': []
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/gear/mesh', methods=['POST'])
def mesh_gears():
    """Analyser l'engrènement de deux engrenages"""
    try:
        data = request.get_json()
        
        if 'gear1' not in data or 'gear2' not in data:
            return jsonify({'error': 'Deux engrenages requis'}), 400
        
        gear1 = GearFactory.from_dict(data['gear1'])
        gear2 = GearFactory.from_dict(data['gear2'])
        
        # Calculer l'engrènement
        center_distance, contact_ratio = gear1.mesh_with(gear2)
        
        # Ratio de transmission
        transmission_ratio = gear2.params.teeth / gear1.params.teeth
        
        return jsonify({
            'success': True,
            'mesh_analysis': {
                'center_distance': center_distance,
                'contact_ratio': contact_ratio,
                'transmission_ratio': transmission_ratio,
                'gear1_info': gear1.get_info(),
                'gear2_info': gear2.get_info()
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/gear/validate', methods=['POST'])
def validate_gear():
    """Valider les paramètres d'un engrenage"""
    try:
        data = request.get_json()
        
        if 'params' not in data:
            return jsonify({'error': 'Paramètres requis'}), 400
        
        params = GearParams(**data['params'])
        
        from core.validation import GearValidator
        errors = GearValidator.validate_gear_params(params)
        
        return jsonify({
            'success': True,
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': [] if len(errors) == 0 else ['Vérifiez les paramètres']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/export/step', methods=['POST'])
def export_step():
    """Exporter un engrenage en STEP"""
    try:
        data = request.get_json()
        
        if 'gear' not in data:
            return jsonify({'error': 'Configuration d\'engrenage requise'}), 400
        
        gear = GearFactory.from_dict(data['gear'])
        
        from export.step import STEPExporter
        exporter = STEPExporter()
        
        filename = data.get('filename', 'gear_export.step')
        exporter.export_gear(gear, filename)
        
        return jsonify({
            'success': True,
            'message': f'Fichier STEP généré: {filename}',
            'download_url': f'/downloads/{filename}'  # À implémenter
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Documentation de l'API
@app.route('/api/docs', methods=['GET'])
def api_docs():
    """Documentation de l'API"""
    docs = {
        'endpoints': {
            '/api/health': 'GET - Vérifier l\'état du service',
            '/api/gear/types': 'GET - Liste des types d\'engrenages',
            '/api/gear/create': 'POST - Créer un engrenage',
            '/api/gear/analyze': 'POST - Analyser un engrenage',
            '/api/gear/mesh': 'POST - Analyser un engrènement',
            '/api/gear/validate': 'POST - Valider des paramètres',
            '/api/export/step': 'POST - Exporter en STEP'
        },
        'example_request': {
            'create_gear': {
                'type': 'spur',
                'params': {
                    'name': 'MyGear',
                    'module': 2.0,
                    'teeth': 20,
                    'pressure_angle': 20.0
                }
            }
        }
    }
    return jsonify(docs)

def run_api(host='0.0.0.0', port=5000, debug=False):
    """Démarrer l'API"""
    print(f"Démarrage de l'API Gear Engine sur {host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_api(debug=True)