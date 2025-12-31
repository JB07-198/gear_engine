/**
 * Main Application Logic
 * Handles page navigation and initialization
 */

class GearEngineApp {
    constructor() {
        this.currentSection = 'home';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.detectAPIServer();
        document.body.classList.add('loaded');
    }

    setupEventListeners() {
        // Navigation links
        document.querySelectorAll('[data-section]').forEach((link) => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.dataset.section;
                this.navigateToSection(section);
            });
        });

        // Hamburger menu
        const hamburger = document.getElementById('hamburger');
        const mobileNav = document.getElementById('mobileNav');

        hamburger?.addEventListener('click', () => {
            mobileNav?.classList.toggle('open');
            hamburger.classList.toggle('open');
        });

        // Close mobile menu when link is clicked
        document.querySelectorAll('.mobile-nav-link').forEach((link) => {
            link.addEventListener('click', () => {
                mobileNav?.classList.remove('open');
                hamburger?.classList.remove('open');
            });
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                if (e.key === '1') this.navigateToSection('home');
                if (e.key === '2') this.navigateToSection('generator');
                if (e.key === '3') this.navigateToSection('documentation');
                if (e.key === '4') this.navigateToSection('about');
            }
        });
    }

    /**
     * Navigate to a section
     */
    navigateToSection(section) {
        // Hide all sections
        document.querySelectorAll('.section').forEach((s) => {
            s.classList.remove('active');
        });

        // Show target section
        const targetSection = document.getElementById(section);
        if (targetSection) {
            targetSection.classList.add('active');
            this.currentSection = section;

            // Update active nav link
            document.querySelectorAll('[data-section]').forEach((link) => {
                link.classList.remove('active');
                if (link.dataset.section === section) {
                    link.classList.add('active');
                }
            });

            // Scroll to top
            window.scrollTo(0, 0);
        }
    }

    /**
     * Detect API server and set correct base URL
     */
    async detectAPIServer() {
        const endpoints = [
            'http://localhost:3000',
            'http://localhost:5000',
            'https://gear-api.herokuapp.com',
            'https://api.gearengine.dev',
        ];

        for (const endpoint of endpoints) {
            try {
                const response = await fetch(`${endpoint}/api/health`, {
                    method: 'GET',
                    timeout: 2000,
                });

                if (response.ok) {
                    apiClient.setBaseUrl(`${endpoint}/api`);
                    console.log(`API server detected at: ${endpoint}`);
                    return;
                }
            } catch (error) {
                // Continue to next endpoint
            }
        }

        // If no server found, show a warning in console
        console.warn('No API server detected. Some features may not work.');
        console.warn(
            'Please ensure the backend is running at one of these URLs:',
            endpoints
        );
    }

    /**
     * Check if API is available
     */
    async checkAPIAvailability() {
        try {
            const result = await apiClient.healthCheck();
            return result.status === 'ok';
        } catch (error) {
            return false;
        }
    }

    /**
     * Show API error banner
     */
    showAPIErrorBanner() {
        const banner = document.createElement('div');
        banner.className = 'alert alert-error';
        banner.style.margin = '1rem';
        banner.innerHTML = `
            <strong>API Server Not Available:</strong> The backend server is not running.
            Please check that it's started and accessible. 
            <a href="https://github.com/yourusername/gear_engine" target="_blank" style="color: inherit;">
                See deployment guide
            </a>
        `;
        document.body.prepend(banner);
    }
}

// Global app instance
let app = null;

/**
 * Navigate to section (global function for onclick handlers)
 */
function navigateToSection(section) {
    if (app) {
        app.navigateToSection(section);
    }
}

/**
 * Initialize app when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    app = new GearEngineApp();
});

/**
 * Handle beforeunload to warn unsaved changes
 */
window.addEventListener('beforeunload', (e) => {
    const form = document.getElementById('gearForm');
    if (form && formManager && formManager.isDirty?.()) {
        e.preventDefault();
        e.returnValue = '';
    }
});

/**
 * Utility: Format numbers
 */
function formatNumber(num, decimals = 2) {
    return Number(num).toFixed(decimals);
}

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Utility: Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function (...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), limit);
        }
    };
}

/**
 * Copy to clipboard utility
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (err) {
        console.error('Failed to copy:', err);
        return false;
    }
}

/**
 * LocalStorage helper
 */
const storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Storage error:', e);
        }
    },
    get: (key, defaultValue = null) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('Storage error:', e);
            return defaultValue;
        }
    },
    remove: (key) => {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Storage error:', e);
        }
    },
    clear: () => {
        try {
            localStorage.clear();
        } catch (e) {
            console.error('Storage error:', e);
        }
    },
};

/**
 * Event system for loose coupling
 */
const eventBus = {
    events: {},
    on: function (event, callback) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(callback);
    },
    off: function (event, callback) {
        if (this.events[event]) {
            this.events[event] = this.events[event].filter(
                (cb) => cb !== callback
            );
        }
    },
    emit: function (event, data) {
        if (this.events[event]) {
            this.events[event].forEach((callback) => callback(data));
        }
    },
};

// Custom events
eventBus.on('gear:generated', (data) => {
    console.log('Gear generated:', data);
});

eventBus.on('gear:exported', (data) => {
    console.log('Gear exported:', data);
});

eventBus.on('app:error', (error) => {
    console.error('App error:', error);
});
// Initialize managers on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    // Theme manager is auto-initialized
    if (window.themeManager) {
        console.log('✓ Theme Manager initialized');
    }

    // Presets manager is auto-initialized
    if (window.presetsManager) {
        console.log('✓ Presets Manager initialized');
    }

    // Share manager is auto-initialized
    if (window.shareManager) {
        console.log('✓ Share Manager initialized');
    }

    // Setup FAQ toggle functionality
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', function() {
            this.parentElement.classList.toggle('open');
        });
    });

    // Initialize app
    app = new GearEngineApp();
    console.log('✓ Gear Engine Application initialized');
});

// Handle page unload with unsaved changes warning
window.addEventListener('beforeunload', (e) => {
    const form = document.getElementById('gearForm');
    if (form && form.classList.contains('modified')) {
        e.preventDefault();
        e.returnValue = '';
    }
});

// Add keyboard shortcuts help
const KEYBOARD_SHORTCUTS = {
    '⌘/Ctrl + 1': 'Go to Home',
    '⌘/Ctrl + 2': 'Go to Generator',
    '⌘/Ctrl + 3': 'Go to Documentation',
    '⌘/Ctrl + 4': 'Go to About',
    '?': 'Show this help'
};

document.addEventListener('keydown', (e) => {
    if (e.key === '?' && !e.ctrlKey && !e.metaKey) {
        let message = 'Keyboard Shortcuts:\n\n';
        Object.entries(KEYBOARD_SHORTCUTS).forEach(([shortcut, action]) => {
            message += `${shortcut}: ${action}\n`;
        });
        console.log(message);
    }
});