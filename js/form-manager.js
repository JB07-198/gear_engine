/**
 * Form Manager for Gear Parameters
 * Handles dynamic form switching and validation
 */

class FormManager {
    constructor() {
        this.currentGearType = 'spur';
        this.gearTypes = [
            'spur',
            'helical',
            'bevel',
            'internal',
            'planetary',
            'rack',
            'worm',
        ];
        this.HISTORY_KEY = 'gearEngine_history';
        this.history = this.loadHistory();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.displayHistory();
    }

    setupEventListeners() {
        // Gear type buttons
        document.querySelectorAll('.gear-type-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => this.onGearTypeChange(e));
        });

        // Form buttons
        document.getElementById('generateBtn')?.addEventListener('click', () =>
            this.onGenerateClick()
        );
        document.getElementById('resetBtn')?.addEventListener('click', () =>
            this.onResetClick()
        );

        // Export buttons
        document.getElementById('downloadStepBtn')?.addEventListener('click', () =>
            this.onExportStep()
        );
        document.getElementById('downloadStlBtn')?.addEventListener('click', () =>
            this.onExportStl()
        );

        // Reset view button
        document.getElementById('resetViewBtn')?.addEventListener('click', () =>
            this.onResetView()
        );
    }

    /**
     * Handle gear type change
     */
    onGearTypeChange(event) {
        const gearType = event.target.dataset.type;
        if (!gearType || !this.gearTypes.includes(gearType)) return;

        this.currentGearType = gearType;

        // Update active button
        document.querySelectorAll('.gear-type-btn').forEach((btn) => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');

        // Show/hide relevant parameters
        document.querySelectorAll('.param-group').forEach((group) => {
            group.classList.remove('active');
        });
        const paramGroup = document.getElementById(`${gearType}-params`);
        if (paramGroup) {
            paramGroup.classList.add('active');
        }
    }

    /**
     * Get current form data
     */
    getFormData() {
        const form = document.getElementById('gearForm');
        const formData = new FormData(form);
        const data = {};

        for (let [key, value] of formData.entries()) {
            data[key] = parseFloat(value) || value;
        }

        return data;
    }

    /**
     * Validate form data
     */
    async validateForm() {
        const data = this.getFormData();

        try {
            const result = await apiClient.validateParameters(
                this.currentGearType,
                data
            );
            return result;
        } catch (error) {
            console.error('Validation error:', error);
            return { valid: false, errors: [error.message] };
        }
    }

    /**
     * Handle generate button click
     */
    async onGenerateClick() {
        // Clear previous messages
        this.hideMessages();

        // Show loading screen
        const loadingScreen = document.getElementById('loadingScreen');
        if (loadingScreen) {
            loadingScreen.classList.add('show');
        }

        try {
            // Validate form
            const validation = await this.validateForm();
            if (!validation.valid) {
                throw new Error(
                    validation.errors?.join(', ') ||
                        'Validation failed. Check your parameters.'
                );
            }

            // Get form data
            const parameters = this.getFormData();

            // Generate gear
            const result = await apiClient.generateGear(
                this.currentGearType,
                parameters
            );

            if (!result || !result.success) {
                throw new Error(result.error || 'Generation failed');
            }

            // Display gear
            this.displayGear(result);

            // Update properties
            this.updateProperties(result);

            // Enable export buttons
            this.enableExportButtons();

            // Add to history
            this.addToHistory(this.currentGearType, parameters);

            // Show success message
            this.showMessage('Gear generated successfully!', 'success');
        } catch (error) {
            console.error('Generation error:', error);
            this.showMessage(
                error.message || 'Failed to generate gear',
                'error'
            );
        } finally {
            const loadingScreen = document.getElementById('loadingScreen');
            if (loadingScreen) {
                loadingScreen.classList.remove('show');
            }
        }
    }

    /**
     * Handle reset button click
     */
    onResetClick() {
        document.getElementById('gearForm')?.reset();
        this.hideMessages();
    }

    /**
     * Handle export STEP
     */
    async onExportStep() {
        try {
            const gearData = this.getCurrentGearData();
            if (!gearData) {
                throw new Error('No gear generated yet');
            }

            const spinner = document.getElementById('loadingSpinner');
            if (spinner) spinner.style.display = 'flex';

            const blob = await apiClient.exportStep(gearData);
            const filename = `gear_${this.currentGearType}_${Date.now()}.step`;
            apiClient.downloadFile(blob, filename);

            this.showMessage('STEP file downloaded successfully!', 'success');
        } catch (error) {
            console.error('Export error:', error);
            this.showMessage(error.message || 'Export failed', 'error');
        } finally {
            const spinner = document.getElementById('loadingSpinner');
            if (spinner) spinner.style.display = 'none';
        }
    }

    /**
     * Handle export STL
     */
    async onExportStl() {
        try {
            const gearData = this.getCurrentGearData();
            if (!gearData) {
                throw new Error('No gear generated yet');
            }

            const spinner = document.getElementById('loadingSpinner');
            if (spinner) spinner.style.display = 'flex';

            const blob = await apiClient.exportStl(gearData);
            const filename = `gear_${this.currentGearType}_${Date.now()}.stl`;
            apiClient.downloadFile(blob, filename);

            this.showMessage('STL file downloaded successfully!', 'success');
        } catch (error) {
            console.error('Export error:', error);
            this.showMessage(error.message || 'Export failed', 'error');
        } finally {
            const spinner = document.getElementById('loadingSpinner');
            if (spinner) spinner.style.display = 'none';
        }
    }

    /**
     * Handle reset view
     */
    onResetView() {
        if (gearViewer) {
            gearViewer.resetView();
        }
    }

    /**
     * Display gear in 3D viewer
     */
    displayGear(gearData) {
        const canvas = document.getElementById('canvas3d');
        if (!canvas) return;

        if (!gearViewer) {
            gearViewer = new GearViewer3D(canvas);
        }

        gearViewer.displayGear(gearData);
    }

    /**
     * Update gear properties display
     */
    updateProperties(gearData) {
        const container = document.getElementById('propertiesContent');
        if (!container) return;

        let html = '';

        if (gearData.properties) {
            for (const [key, value] of Object.entries(gearData.properties)) {
                const label = this.formatPropertyLabel(key);
                const displayValue = this.formatPropertyValue(value);
                html += `
                    <div class="property-item">
                        <div class="property-label">${label}</div>
                        <div class="property-value">${displayValue}</div>
                    </div>
                `;
            }
        }

        container.innerHTML = html || '<p class="placeholder-text">No properties available</p>';
    }

    /**
     * Format property label
     */
    formatPropertyLabel(key) {
        return key
            .split('_')
            .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    /**
     * Format property value
     */
    formatPropertyValue(value) {
        if (typeof value === 'number') {
            return value.toFixed(2);
        }
        return String(value);
    }

    /**
     * Enable export buttons
     */
    enableExportButtons() {
        const stepBtn = document.getElementById('downloadStepBtn');
        const stlBtn = document.getElementById('downloadStlBtn');

        if (stepBtn) stepBtn.disabled = false;
        if (stlBtn) stlBtn.disabled = false;
    }

    /**
     * Disable export buttons
     */
    disableExportButtons() {
        const stepBtn = document.getElementById('downloadStepBtn');
        const stlBtn = document.getElementById('downloadStlBtn');

        if (stepBtn) stepBtn.disabled = true;
        if (stlBtn) stlBtn.disabled = true;
    }

    /**
     * Show message
     */
    showMessage(message, type = 'error') {
        const errorMsg = document.getElementById('errorMessage');
        const successMsg = document.getElementById('successMessage');

        if (type === 'error' && errorMsg) {
            errorMsg.textContent = message;
            errorMsg.style.display = 'block';
            successMsg.style.display = 'none';
        } else if (type === 'success' && successMsg) {
            successMsg.textContent = message;
            successMsg.style.display = 'block';
            errorMsg.style.display = 'none';
        }

        // Auto-hide after 5 seconds
        setTimeout(() => this.hideMessages(), 5000);
    }

    /**
     * Hide messages
     */
    hideMessages() {
        const errorMsg = document.getElementById('errorMessage');
        const successMsg = document.getElementById('successMessage');

        if (errorMsg) errorMsg.style.display = 'none';
        if (successMsg) successMsg.style.display = 'none';
    }

    /**
     * Get current gear data
     */
    getCurrentGearData() {
        // This would be set when a gear is generated
        return window.currentGearData || null;
    }

    /**
     * Set current gear data
     */
    setCurrentGearData(data) {
        window.currentGearData = data;
    }

    /**
     * Add to generation history
     */
    addToHistory(gearType, parameters) {
        const entry = {
            id: Date.now(),
            gearType,
            parameters,
            timestamp: new Date().toISOString(),
            displayName: `${gearType.charAt(0).toUpperCase() + gearType.slice(1)} - ${new Date().toLocaleTimeString()}`
        };

        this.history.unshift(entry);
        if (this.history.length > 20) {
            this.history.pop(); // Keep only last 20
        }

        this.persistHistory();
        this.displayHistory();

        if (window.eventBus) {
            eventBus.emit('generation-added-to-history', { entry });
        }
    }

    /**
     * Load a previous generation from history
     */
    loadFromHistory(id) {
        const entry = this.history.find(h => h.id === id);
        if (!entry) return;

        // Set gear type
        const gearTypeSelect = document.getElementById('gearType');
        if (gearTypeSelect) {
            gearTypeSelect.value = entry.gearType;
            gearTypeSelect.dispatchEvent(new Event('change'));
        }

        // Set parameters
        setTimeout(() => {
            Object.entries(entry.parameters).forEach(([key, value]) => {
                const input = document.getElementById(key);
                if (input && input.type !== 'hidden') {
                    input.value = value;
                }
            });
        }, 100);
    }

    /**
     * Display generation history
     */
    displayHistory() {
        if (this.history.length === 0) return;

        let historyPanel = document.getElementById('historyPanel');
        
        if (!historyPanel) {
            const generatorLeft = document.querySelector('.generator-left');
            if (!generatorLeft) return;

            historyPanel = document.createElement('div');
            historyPanel.id = 'historyPanel';
            historyPanel.className = 'history-panel';
            generatorLeft.insertBefore(historyPanel, generatorLeft.firstChild);
        }

        historyPanel.innerHTML = `
            <div class="history-title">📋 Recent Generations (${this.history.length})</div>
            ${this.history.slice(0, 5).map(entry => `
                <div class="history-item" onclick="formManager.loadFromHistory(${entry.id})" title="Load this design">
                    ${entry.displayName}
                </div>
            `).join('')}
            ${this.history.length > 5 ? `<div class="history-title" style="font-size: 12px; margin-top: 8px;">+${this.history.length - 5} more...</div>` : ''}
        `;
    }

    /**
     * Load history from localStorage
     */
    loadHistory() {
        try {
            const data = localStorage.getItem(this.HISTORY_KEY);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            console.error('Error loading history:', e);
            return [];
        }
    }

    /**
     * Persist history to localStorage
     */
    persistHistory() {
        try {
            localStorage.setItem(this.HISTORY_KEY, JSON.stringify(this.history));
        } catch (e) {
            console.error('Error saving history:', e);
        }
    }

    /**
     * Clear all history
     */
    clearHistory() {
        if (confirm('Clear all generation history?')) {
            this.history = [];
            this.persistHistory();
            const panel = document.getElementById('historyPanel');
            if (panel) panel.remove();
        }
    }

    /**
     * Get history
     */
    getHistory() {
        return [...this.history];
    }

// Create global form manager instance and expose to window for other scripts
window.formManager = new FormManager();
