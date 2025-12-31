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
        const designParams = params.get('design');

        if (!designParams) return;

        try {
            const urlParams = new URLSearchParams(designParams);
            const gearType = urlParams.get('type');

            if (!gearType) return;

            // Set gear type
            const gearTypeSelect = document.getElementById('gearType');
            if (gearTypeSelect) {
                gearTypeSelect.value = gearType;
                gearTypeSelect.dispatchEvent(new Event('change'));
            }

            // Set parameters
            setTimeout(() => {
                urlParams.forEach((value, key) => {
                    if (key !== 'type') {
                        const input = document.getElementById(key);
                        if (input) {
                            input.value = value;
                        }
                    }
                });

                // Show notification
                const msg = document.createElement('div');
                msg.style.cssText = `
                    background: var(--primary-color);
                    color: white;
                    padding: 12px 16px;
                    border-radius: var(--radius-md);
                    margin-bottom: 15px;
                    font-size: 14px;
                `;
                msg.textContent = '✓ Design loaded from shared link';
                document.querySelector('.generator-left').insertBefore(msg, document.querySelector('.param-group'));

                setTimeout(() => msg.remove(), 3000);

                if (window.eventBus) {
                    eventBus.emit('design-loaded', { gearType, parameters: Object.fromEntries(urlParams) });
                }
            }, 100);

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
