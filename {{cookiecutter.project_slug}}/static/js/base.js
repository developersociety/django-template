var main = document.querySelector('.main');

// Stretch main to fill height of screen minus header and footer
if (main) {
    var footer_height = document.querySelector('.footer').offsetHeight;
    var header_height = document.querySelector('.header').offsetHeight;
    var total_height = header_height + footer_height;
    main.style.minHeight = `${window.innerHeight - total_height}px`;
}
