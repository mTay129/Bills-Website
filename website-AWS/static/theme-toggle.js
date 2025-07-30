// /static/theme-toggle.js

document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('theme-toggle');
    const isDark = localStorage.getItem('theme') === 'dark';

    if (isDark) {
        document.body.classList.add('dark-theme');
    }

    toggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        const currentTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
        localStorage.setItem('theme', currentTheme);
    });
});