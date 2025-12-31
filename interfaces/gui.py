import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from core.gear_factory import GearFactory
from core.base_gear import GearParams
from export.step import STEPExporter


def _create_gear_from_fields(fields):
    try:
        params = {
            'name': fields['name'].get(),
            'module': float(fields['module'].get()),
            'teeth': int(fields['teeth'].get()),
            'pressure_angle': float(fields['pressure_angle'].get()),
            'face_width': float(fields['face_width'].get()),
        }
        # optional leads
        leads_val = fields.get('leads')
        if leads_val and leads_val.get():
            params['leads'] = int(leads_val.get())

        return params
    except Exception as e:
        raise


def run_gui():
    root = tk.Tk()
    root.title('Gear Engine - GUI (Demo)')

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    # Fields
    labels = ['Type', 'Name', 'Module', 'Teeth', 'Pressure angle', 'Face width', 'Leads']
    entries = {}

    gear_types = ['spur', 'helical', 'bevel', 'worm', 'rack', 'internal']
    ttk.Label(frame, text='Type').grid(row=0, column=0, sticky=tk.W)
    type_cb = ttk.Combobox(frame, values=gear_types)
    type_cb.set('spur')
    type_cb.grid(row=0, column=1, sticky=(tk.W, tk.E))
    entries['type'] = type_cb

    for i, label in enumerate(labels[1:], start=1):
        ttk.Label(frame, text=label).grid(row=i, column=0, sticky=tk.W)
        ent = ttk.Entry(frame)
        ent.grid(row=i, column=1, sticky=(tk.W, tk.E))
        key = label.lower().split()[0]
        entries[key] = ent

    # Default values
    entries['name'].insert(0, 'GUIGear')
    entries['module'].insert(0, '2.0')
    entries['teeth'].insert(0, '20')
    entries['pressure'].insert(0, '20.0')
    entries['face'].insert(0, '10.0')

    # Map nicer keys
    fields = {
        'type': entries['type'],
        'name': entries['name'],
        'module': entries['module'],
        'teeth': entries['teeth'],
        'pressure_angle': entries['pressure'],
        'face_width': entries['face'],
        'leads': entries.get('leads')
    }

    # Output text
    output = tk.Text(frame, height=10, width=60)
    output.grid(row=8, column=0, columnspan=2, pady=(10, 0))

    def append(msg):
        output.insert(tk.END, msg + '\n')
        output.see(tk.END)

    def on_create():
        try:
            params_dict = _create_gear_from_fields(fields)
            gear_type = fields['type'].get()
            params = GearParams(**params_dict)
            # ensure types registered
            from gears.spur import SpurGear
            from gears.helical import HelicalGear
            from gears.bevel import BevelGear
            from gears.worm import WormGear
            from gears.rack import RackGear
            from gears.internal import InternalGear
            GearFactory.register_gear('spur', SpurGear)
            GearFactory.register_gear('helical', HelicalGear)
            GearFactory.register_gear('bevel', BevelGear)
            GearFactory.register_gear('worm', WormGear)
            GearFactory.register_gear('rack', RackGear)
            GearFactory.register_gear('internal', InternalGear)

            gear = GearFactory.create_gear(gear_type, params)
            info = gear.get_info()
            append('Engrenage créé: ' + info.get('name', ''))
            for k, v in info.items():
                append(f"{k}: {v}")
        except Exception as e:
            messagebox.showerror('Erreur', str(e))

    def on_export():
        try:
            params_dict = _create_gear_from_fields(fields)
            gear_type = fields['type'].get()
            params = GearParams(**params_dict)
            gear = GearFactory.create_gear(gear_type, params)
            filename = filedialog.asksaveasfilename(defaultextension='.step', filetypes=[('STEP','*.step')])
            if not filename:
                return
            exporter = STEPExporter()
            exporter.export_gear(gear, filename)
            append(f'Fichier STEP généré: {filename}')
        except Exception as e:
            messagebox.showerror('Erreur', str(e))

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=7, column=0, columnspan=2, pady=(8, 0))
    ttk.Button(btn_frame, text='Create', command=on_create).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text='Export STEP', command=on_export).grid(row=0, column=1, padx=5)

    root.mainloop()


if __name__ == '__main__':
    run_gui()
