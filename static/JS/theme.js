// theme.js

// Function to get the current theme from localStorage or default to 'light'
function getTheme() {
    return localStorage.getItem('theme') || 'light';
}

// Function to set the theme to the document root and store in localStorage
function setTheme(theme) {
    document.documentElement.className = theme;
    localStorage.setItem('theme', theme);
}

// Load the theme when the page loads
window.onload = function() {
    setTheme(getTheme());
};

// Event listener for theme switcher button
document.getElementById('openSwitcher').addEventListener('click', function() {
    const currentTheme = getTheme();
    const newTheme = currentTheme === 'light' ? 'dark' : currentTheme === 'dark' ? 'lightgreen' : 'light';
    setTheme(newTheme);
});
