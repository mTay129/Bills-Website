// static/theme-toggle.js
// Theme toggler: switches between light and dark mode with label updates and localStorage support.

document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("theme-toggle");

    function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
        toggleBtn.textContent = theme === "dark" ? "Light Mode" : "Dark Mode";
    }

    // Load stored theme or default to dark
    const savedTheme = localStorage.getItem("theme") || "dark";
    setTheme(savedTheme);

    // Toggle theme on click
    toggleBtn.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        setTheme(newTheme);
    });
});
