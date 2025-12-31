/**
 * Theme Manager - Dark/Light Mode Toggle
 * Handles theme switching and persistence
 */

class ThemeManager {
    constructor() {
        this.STORAGE_KEY = 'gearEngine_theme';
        this.LIGHT_THEME = 'light-theme';
        this.DARK_THEME = 'dark-theme';
        this.init();
    }

    init() {
        const themeToggle = document.getElementById('themeToggle');
        if (!themeToggle) return;

        // Load saved theme or detect system preference
        const savedTheme = localStorage.getItem(this.STORAGE_KEY);
        if (savedTheme) {
            this.setTheme(savedTheme);
        } else {
            // Detect system preference
            const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.setTheme(isDark ? this.DARK_THEME : this.LIGHT_THEME);
        }

        // Toggle button listener
        themeToggle.addEventListener('click', () => this.toggle());

        // System theme change listener
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem(this.STORAGE_KEY)) {
                this.setTheme(e.matches ? this.DARK_THEME : this.LIGHT_THEME);
            }
        });
    }

    setTheme(theme) {
        const body = document.body;
        const themeToggle = document.getElementById('themeToggle');

        if (theme === this.LIGHT_THEME) {
            body.classList.add(this.LIGHT_THEME);
            body.classList.remove(this.DARK_THEME);
            if (themeToggle) themeToggle.textContent = '🌙';
        } else {
            body.classList.remove(this.LIGHT_THEME);
            body.classList.add(this.DARK_THEME);
            if (themeToggle) themeToggle.textContent = '☀️';
        }

        localStorage.setItem(this.STORAGE_KEY, theme);
        this.emitThemeChangeEvent(theme);
    }

    toggle() {
        const currentTheme = localStorage.getItem(this.STORAGE_KEY) || this.DARK_THEME;
        const newTheme = currentTheme === this.DARK_THEME ? this.LIGHT_THEME : this.DARK_THEME;
        this.setTheme(newTheme);
    }

    getCurrentTheme() {
        return localStorage.getItem(this.STORAGE_KEY) || this.DARK_THEME;
    }

    emitThemeChangeEvent(theme) {
        if (window.eventBus) {
            eventBus.emit('theme-changed', { theme });
        }
    }
}

// Initialize theme manager
const themeManager = new ThemeManager();
