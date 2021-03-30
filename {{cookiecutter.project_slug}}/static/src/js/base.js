import svg4everybody from 'svg4everybody';

const main = document.querySelector('.main');

// Stretch main height to fill the screen
if (main) {
    const footer_height = document.querySelector('.footer').offsetHeight;
    const header_height = document.querySelector('.header').offsetHeight;
    const total_height = header_height + footer_height;
    main.style.minHeight = `${window.innerHeight - total_height}px`;
}

// Polyfill for loading external SVGs in IE
// https://github.com/jonathantneal/svg4everybody
svg4everybody();
