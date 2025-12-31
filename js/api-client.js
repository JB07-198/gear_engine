/**
 * API Client for Gear Engine
 * Handles communication with the backend API
 */

class GearAPIClient {
    constructor(baseUrl = 'http://localhost:5000/api') {
        this.baseUrl = baseUrl;
        this.timeout = 30000; // 30 seconds (not directly used by fetch)
    }

    /**
     * Make an API request
     */
    async request(endpoint, method = 'GET', data = null) {
        const url = `${this.baseUrl}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(
                    errorData.error || `API error: ${response.statusText}`
                );
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    /**
     * Generate a gear
     */
    async generateGear(gearType, parameters) {
        // Server expects { type: <type>, params: <parameters> } at /api/gear/create
        return this.request('/gear/create', 'POST', {
            type: gearType,
            params: parameters,
        });
    }

    /**
     * Export gear to STEP format
     */
    async exportStep(gearData) {
        // Server export endpoint is /api/export/step and expects { gear: ... }
        const url = `${this.baseUrl}/export/step`;
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ gear: gearData }),
            });

            if (!response.ok) {
                throw new Error(`Export failed: ${response.statusText}`);
            }

            return await response.blob();
        } catch (error) {
            console.error('STEP export failed:', error);
            throw error;
        }
    }

    /**
     * Export gear to STL format
     */
    async exportStl(gearData) {
        const url = `${this.baseUrl}/export/stl`;
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ gear: gearData }),
            });

            if (!response.ok) {
                throw new Error(`Export failed: ${response.statusText}`);
            }

            return await response.blob();
        } catch (error) {
            console.error('STL export failed:', error);
            throw error;
        }
    }

    /**
     * Get gear information/properties
     */
    async getGearInfo(gearType, parameters) {
        // Map to server analyze endpoint
        return this.request('/gear/analyze', 'POST', {
            gear: { type: gearType, params: parameters },
        });
    }

    /**
     * Validate parameters for a gear type
     */
    async validateParameters(gearType, parameters) {
        // Server expects { params: {...} }
        return this.request('/gear/validate', 'POST', {
            params: parameters,
        });
    }

    /**
     * Download a file
     */
    downloadFile(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    }

    /**
     * Set base URL (useful for different environments)
     */
    setBaseUrl(url) {
        this.baseUrl = url;
    }

    /**
     * Health check
     */
    async healthCheck() {
        try {
            return await this.request('/health');
        } catch (error) {
            return { status: 'error', message: error.message };
        }
    }
}

// Create global API client instance
const apiClient = new GearAPIClient();
