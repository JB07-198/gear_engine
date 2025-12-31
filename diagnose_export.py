import sys

print("=" * 60)
print("DIAGNOSTIC DES BIBLIOTHÈQUES CAO")
print("=" * 60)
print()

# Liste des bibliothèques potentielles pour la CAO
libs = [
    ('cadquery', 'CadQuery (CAO Python)'),
    ('OCC', 'pythonocc-core (OpenCASCADE)'),
    ('trimesh', 'Trimesh (maillages 3D)'),
    ('solidpython', 'SolidPython'),
    ('scipy.spatial', 'SciPy Spatial'),
    ('stl', 'numpy-stl'),
]

print("Vérification des bibliothèques installées:")
print("-" * 60)

installed = []
missing = []

for lib, desc in libs:
    try:
        __import__(lib)
        print(f"✅ {desc:40} INSTALLÉ")
        installed.append(lib)
    except ImportError:
        print(f"❌ {desc:40} MANQUANT")
        missing.append((lib, desc))

print()
print("=" * 60)
print("INSPECTION DU MODULE EXPORT")
print("=" * 60)
print()

try:
    from export import stl
    import inspect
    
    print(f"📁 Fichier du module STL:")
    print(f"   {stl.__file__}")
    print()
    
    print("📦 Classes disponibles:")
    classes = []
    for name, obj in inspect.getmembers(stl, inspect.isclass):
        print(f"   - {name}")
        classes.append(name)
    
    print()
    print("🔧 Fonctions disponibles:")
    functions = []
    for name, obj in inspect.getmembers(stl, inspect.isfunction):
        print(f"   - {name}")
        functions.append(name)
        
except Exception as e:
    print(f"❌ Erreur lors de l'inspection: {e}")

print()
print("=" * 60)
print("RÉSUMÉ")
print("=" * 60)
print(f"Bibliothèques installées: {len(installed)}")
print(f"Bibliothèques manquantes: {len(missing)}")

if missing:
    print()
    print("💡 Pour installer les bibliothèques manquantes:")
    print()
    for lib, desc in missing:
        if lib == 'trimesh':
            print(f"   pip install trimesh")
        elif lib == 'cadquery':
            print(f"   pip install cadquery")
        elif lib == 'OCC':
            print(f"   conda install -c conda-forge pythonocc-core")
        elif lib == 'stl':
            print(f"   pip install numpy-stl")
            
print()
print("=" * 60)
