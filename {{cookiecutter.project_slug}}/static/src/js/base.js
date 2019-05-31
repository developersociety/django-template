const main = document.querySelector('.main');
console.log('main', main)

// Stretch main to fill height of screen minus header and footer
if (main) {
    const footer_height = document.querySelector('.footer').offsetHeight;
    const header_height = document.querySelector('.header').offsetHeight;
    const total_height = header_height + footer_height;
    main.style.minHeight = `${window.innerHeight - total_height}px`;
}
