// static/theme-toggle.js
// This script toggles the theme between light and dark modes
// and updates the label accordingly.

document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("theme-toggle");

    function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
        toggleBtn.textContent = theme === "dark" ? "Light Mode" : "Dark Mode";
    }

    // Load saved theme
    const savedTheme = localStorage.getItem("theme") || "dark";
    setTheme(savedTheme);

    // Toggle on click
    toggleBtn.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        setTheme(newTheme);
    });
});

// Update the label based on the current theme
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