// Theme handling. The class lives on <html> (set early by the inline script in <head>
// to avoid a flash of the wrong theme), and the choice is kept in localStorage.
(function () {
    const root = document.documentElement;
    const KEY = 'theme';

    function stored() {
        try {
            return window.localStorage.getItem(KEY) === 'dark' ? 'dark' : 'light';
        } catch (_) {
            return 'light';
        }
    }

    function apply(theme) {
        root.classList.toggle('dark-mode', theme === 'dark');

        document.querySelectorAll('[data-theme-value]').forEach((button) => {
            button.setAttribute('aria-pressed', String(button.dataset.themeValue === theme));
        });

        const toggle = document.getElementById('theme-toggle');
        if (toggle) toggle.textContent = theme === 'dark' ? '☀️' : '🌙';
    }

    function setTheme(theme) {
        try {
            window.localStorage.setItem(KEY, theme);
        } catch (_) { /* storage unavailable: the theme just won't be remembered */ }

        apply(theme);
    }

    window.setTheme = setTheme;
    apply(stored());

    document.addEventListener('click', (e) => {
        const choice = e.target.closest('[data-theme-value]');
        if (choice) setTheme(choice.dataset.themeValue);

        if (e.target.closest('#theme-toggle')) setTheme(stored() === 'dark' ? 'light' : 'dark');
    });
})();
