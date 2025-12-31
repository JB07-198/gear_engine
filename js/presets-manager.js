/**
 * Presets Manager - Save/Load Parameter Presets
 * Handles localStorage-based preset management
 */

class PresetsManager {
    constructor() {
        this.STORAGE_KEY = 'gearEngine_presets';
        this.presets = this.loadPresets();
        this.init();
    }

    init() {
        // Listen for form changes to enable save button
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn) {
            const savePresetBtn = document.createElement('button');
            savePresetBtn.className = 'btn btn-secondary btn-sm';
            savePresetBtn.textContent = '💾 Save Preset';
            savePresetBtn.id = 'savePresetBtn';
            savePresetBtn.style.marginLeft = '10px';
            generateBtn.parentElement.insertBefore(savePresetBtn, generateBtn.nextSibling);
            
            savePresetBtn.addEventListener('click', () => this.showSaveDialog());
        }

        // Add preset selector
        this.createPresetSelector();
    }

    createPresetSelector() {
        if (this.presets.length === 0) return;

        const generatorLeft = document.querySelector('.generator-left');
        if (!generatorLeft) return;

        const selector = document.createElement('div');
        selector.className = 'preset-selector';
        selector.style.marginBottom = '20px';
        
        selector.innerHTML = `
            <label style="display: block; color: var(--text-secondary); font-size: 12px; margin-bottom: 8px;">
                Load Preset:
            </label>
            <div style="display: flex; gap: 10px;">
                <select id="presetSelect" class="input" style="flex: 1;">
                    <option value="">-- Select a preset --</option>
                    ${this.presets.map((p, i) => 
                        `<option value="${i}">${p.name}</option>`
                    ).join('')}
                </select>
                <button class="btn btn-tertiary btn-sm" id="deletePresetBtn" style="padding: 6px 8px;">🗑️</button>
            </div>
        `;

        generatorLeft.insertBefore(selector, generatorLeft.firstChild);

        document.getElementById('presetSelect').addEventListener('change', (e) => {
            if (e.target.value) {
                this.loadPreset(parseInt(e.target.value));
            }
        });

        document.getElementById('deletePresetBtn').addEventListener('click', () => {
            const idx = document.getElementById('presetSelect').value;
            if (idx) this.deletePreset(parseInt(idx));
        });
    }

    showSaveDialog() {
        const name = prompt('Preset name:', `Preset ${this.presets.length + 1}`);
        if (!name) return;

        if (formManager && formManager.getCurrentGearData) {
            const data = formManager.getCurrentGearData();
            this.savePreset(name, data);
            alert(`Preset "${name}" saved!`);
        }
    }

    savePreset(name, data) {
        const preset = {
            name,
            gearType: data.gear_type,
            parameters: data,
            timestamp: new Date().toISOString()
        };

        this.presets.push(preset);
        this.persistPresets();
        this.createPresetSelector();
        
        if (window.eventBus) {
            eventBus.emit('preset-saved', { preset });
        }
    }

    loadPreset(index) {
        const preset = this.presets[index];
        if (!preset) return;

        // Set gear type
        const gearTypeSelect = document.getElementById('gearType');
        if (gearTypeSelect) {
            gearTypeSelect.value = preset.gearType;
            gearTypeSelect.dispatchEvent(new Event('change'));
        }

        // Set parameters
        setTimeout(() => {
            Object.entries(preset.parameters).forEach(([key, value]) => {
                const input = document.getElementById(key);
                if (input && input.type !== 'hidden') {
                    input.value = value;
                }
            });

            if (window.eventBus) {
                eventBus.emit('preset-loaded', { preset });
            }
        }, 100);
    }

    deletePreset(index) {
        if (!confirm(`Delete preset "${this.presets[index].name}"?`)) return;
        
        this.presets.splice(index, 1);
        this.persistPresets();
        this.createPresetSelector();
    }

    loadPresets() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEY);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            console.error('Error loading presets:', e);
            return [];
        }
    }

    persistPresets() {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.presets));
        } catch (e) {
            console.error('Error saving presets:', e);
        }
    }

    getPresets() {
        return [...this.presets];
    }

    getPresetByName(name) {
        return this.presets.find(p => p.name === name);
    }

    exportPresets() {
        const dataStr = JSON.stringify(this.presets, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'gear-presets.json';
        link.click();
        URL.revokeObjectURL(url);
    }

    importPresets(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const imported = JSON.parse(e.target.result);
                if (Array.isArray(imported)) {
                    this.presets = [...this.presets, ...imported];
                    this.persistPresets();
                    this.createPresetSelector();
                    alert('Presets imported successfully!');
                }
            } catch (err) {
                alert('Error importing presets: ' + err.message);
            }
        };
        reader.readAsText(file);
    }
}

// Initialize presets manager
const presetsManager = new PresetsManager();
