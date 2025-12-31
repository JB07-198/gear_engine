/**
 * Share Manager - Share/Load Designs via URL Parameters
 * Encodes gear parameters in URL for sharing
 */

class ShareManager {
    constructor() {
        this.init();
    }

    init() {
        // Add share button to generator
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn) {
            const shareBtn = document.createElement('button');
            shareBtn.className = 'btn btn-tertiary btn-sm';
            shareBtn.textContent = '🔗 Share Design';
            shareBtn.id = 'shareBtn';
            shareBtn.style.marginLeft = '10px';
            shareBtn.addEventListener('click', () => this.shareCurrentDesign());
            generateBtn.parentElement.appendChild(shareBtn);
        }

        // Load design from URL on page load
        this.loadDesignFromURL();
    }

    generateShareURL(gearData) {
        const params = new URLSearchParams();
        
        // Add gear type
        if (gearData.gear_type) {
            params.append('type', gearData.gear_type);
        }

        // Add all parameters
        Object.entries(gearData).forEach(([key, value]) => {
            if (key !== 'gear_type' && value !== undefined && value !== '') {
                params.append(key, value);
            }
        });

        const baseURL = window.location.origin + window.location.pathname;
        return `${baseURL}?design=${params.toString()}`;
    }

    shareCurrentDesign() {
        if (!formManager || !formManager.getCurrentGearData) {
            alert('Please generate a gear first');
            return;
        }

        const gearData = formManager.getCurrentGearData();
        const shareURL = this.generateShareURL(gearData);

        // Copy to clipboard
        navigator.clipboard.writeText(shareURL).then(() => {
            alert('Design link copied to clipboard!');
            
            // Show share options
            this.showShareDialog(shareURL);
        }).catch(() => {
            // Fallback: show URL in dialog
            this.showShareDialog(shareURL);
        });

        if (window.eventBus) {
            eventBus.emit('design-shared', { url: shareURL, gearData });
        }
    }

    showShareDialog(url) {
        const dialog = document.createElement('div');
        dialog.className = 'modal show';
        dialog.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Share Design</h2>
                    <button class="modal-close">&times;</button>
                </div>
                <p style="color: var(--text-secondary); margin-bottom: 15px;">
                    Share this link with others to show them your gear design:
                </p>
                <div style="background: var(--dark-bg); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 12px; margin-bottom: 15px; word-break: break-all;">
                    <code style="color: var(--primary-color); font-size: 12px;">${url}</code>
                </div>
                <div style="display: flex; gap: 10px;">
                    <button class="btn btn-primary" onclick="this.closest('.modal').remove(); navigator.clipboard.writeText('${url}');">
                        📋 Copy Link
                    </button>
                    <a href="${url}" class="btn btn-secondary" target="_blank">
                        🔗 Open Link
                    </a>
                </div>
            </div>
        `;

        document.body.appendChild(dialog);
        dialog.querySelector('.modal-close').addEventListener('click', () => dialog.remove());
        dialog.addEventListener('click', (e) => {
            if (e.target === dialog) dialog.remove();
        });
    }

    loadDesignFromURL() {
        const params = new URLSearchParams(window.location.search);

        // Support both ?design=type=... encoded param and direct query params (?teeth=20&module=2...)
        const designParams = params.get('design');

        let urlParams;
        if (designParams) {
            try {
                urlParams = new URLSearchParams(designParams);
            } catch (e) {
                console.error('Error parsing design param:', e);
                return;
            }
        } else if (params && params.toString()) {
            // Use direct query params
            urlParams = params;
        } else {
            return;
        }

        try {
            // Determine gear type: explicit 'type' or infer from keys
            let gearType = urlParams.get('type') || urlParams.get('gear_type');

            if (!gearType) {
                // Heuristics to infer gear type from parameters
                const keys = Array.from(urlParams.keys());
                if (keys.includes('helix_angle') || keys.includes('helixAngle') || keys.includes('helix')) {
                    gearType = 'helical';
                } else if (keys.includes('pitch_angle') || keys.includes('pitchAngle')) {
                    gearType = 'bevel';
                } else if (keys.includes('rim_thickness')) {
                    gearType = 'internal';
                } else if (keys.includes('sun_teeth') || keys.includes('ring_teeth') || keys.includes('num_planets') || keys.includes('planet_teeth')) {
                    gearType = 'planetary';
                } else if (keys.includes('length') && keys.includes('height') && !keys.includes('teeth')) {
                    gearType = 'rack';
                } else if (keys.includes('threads') || keys.includes('lead_angle')) {
                    gearType = 'worm';
                } else {
                    gearType = 'spur';
                }
            }

            // Switch gear type UI by clicking the corresponding button (keeps behavior consistent)
            const btn = document.querySelector(`.gear-type-btn[data-type="${gearType}"]`);
            if (btn) btn.click();

            // Populate inputs for the selected gear type
            setTimeout(() => {
                const group = document.getElementById(`${gearType}-params`);

                const applied = [];
                urlParams.forEach((value, key) => {
                    if (key === 'type' || key === 'gear_type' || key === 'design') return;

                    // Priority 1: input inside the gear-type group with matching name
                    let input = null;
                    if (group) input = group.querySelector(`[name="${key}"]`) || group.querySelector(`#${gearType}_${key}`);

                    // Priority 2: element with id matching prefixed id
                    if (!input) input = document.getElementById(`${gearType}_${key}`);

                    // Priority 3: any input with name matching key
                    if (!input) input = document.querySelector(`[name="${key}"]`);

                    // Priority 4: direct id match
                    if (!input) input = document.getElementById(key);

                    // Special-case common aliases
                    if (!input) {
                        const aliasMap = {
                            'bore_diameter': 'bore',
                            'face_width': 'face_width',
                            'pressure_angle': 'pressure_angle',
                            'helix_angle': 'helix_angle',
                            'pitch_angle': 'pitch_angle',
                            'rim_thickness': 'rim_thickness',
                            'sun_teeth': 'sun_teeth',
                            'planet_teeth': 'planet_teeth',
                            'ring_teeth': 'ring_teeth',
                            'num_planets': 'num_planets',
                            'threads': 'threads',
                            'lead_angle': 'lead_angle'
                        };
                        const alias = aliasMap[key];
                        if (alias) input = document.getElementById(`${gearType}_${alias}`) || document.querySelector(`#${gearType}-params [name="${alias}"]`);
                    }

                    if (input) {
                        input.value = value;
                        applied.push(key);
                    } else {
                        // console.debug: unmatched param
                        console.debug(`No input found for param '${key}' in gear type '${gearType}'`);
                    }
                });

                // Show notification if any parameters applied
                if (applied.length > 0) {
                    const msg = document.createElement('div');
                    msg.style.cssText = `
                        background: var(--primary-color);
                        color: white;
                        padding: 12px 16px;
                        border-radius: var(--radius-md);
                        margin-bottom: 15px;
                        font-size: 14px;
                    `;
                    msg.textContent = `✓ Loaded ${applied.length} parameter(s) for ${gearType} gear`;
                    document.querySelector('.generator-left').insertBefore(msg, document.querySelector('.param-group'));

                    setTimeout(() => msg.remove(), 3800);

                    // Auto-generate the gear once parameters are loaded
                    if (window.formManager && typeof formManager.onGenerateClick === 'function') {
                        // slight delay to ensure UI updates
                        setTimeout(() => formManager.onGenerateClick(), 200);
                    }
                }

                if (window.eventBus) {
                    eventBus.emit('design-loaded', { gearType, parameters: Object.fromEntries(urlParams) });
                }
            }, 120);

        } catch (e) {
            console.error('Error loading design from URL:', e);
        }
    }

    encodeForURL(obj) {
        return new URLSearchParams(obj).toString();
    }

    decodeFromURL(str) {
        const params = new URLSearchParams(str);
        const obj = {};
        params.forEach((value, key) => {
            obj[key] = value;
        });
        return obj;
    }

    generateQRCode(url) {
        // Simple QR code generation using a QR code API
        // In production, use a proper QR library like qrcode.js
        const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(url)}`;
        return qrUrl;
    }

    showQRCode(url) {
        const qrUrl = this.generateQRCode(url);
        const dialog = document.createElement('div');
        dialog.className = 'modal show';
        dialog.innerHTML = `
            <div class="modal-content" style="text-align: center;">
                <div class="modal-header">
                    <h2>QR Code</h2>
                    <button class="modal-close">&times;</button>
                </div>
                <img src="${qrUrl}" alt="QR Code" style="max-width: 300px; margin: 20px 0;">
                <p style="color: var(--text-secondary); font-size: 12px;">
                    Scan this QR code to share your gear design
                </p>
            </div>
        `;

        document.body.appendChild(dialog);
        dialog.querySelector('.modal-close').addEventListener('click', () => dialog.remove());
    }
}

// Initialize share manager
const shareManager = new ShareManager();
