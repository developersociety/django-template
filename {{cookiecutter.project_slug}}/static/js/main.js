// Watch for user tabbing and enable focus styles if tab key pressed
function handleFirstTab(e) {
    if (e.keyCode === 9) {
        // the "I am a keyboard user" key
        document.body.classList.add("user-tabbing");
        window.removeEventListener("keydown", handleFirstTab);
    }
}

// Listen for scroll on mobile devices to show/hide menu
window.addEventListener("keydown", handleFirstTab);
