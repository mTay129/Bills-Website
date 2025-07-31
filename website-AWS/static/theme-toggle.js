// static/theme-toggle.js
// This script toggles the theme between light and dark modes
// and updates the label accordingly.

document.getElementById('theme-toggle').addEventListener('click', function () {
    document.body.classList.toggle('dark-theme');
    updateThemeLabel();
});

function updateThemeLabel() {
    const label = document.getElementById('theme-toggle');
    if (document.body.classList.contains('dark-theme')) {
        label.textContent = 'Light Mode';
    } else {
        label.textContent = 'Dark Mode';
    }
}

// Ensure label is set correctly on page load
updateThemeLabel();