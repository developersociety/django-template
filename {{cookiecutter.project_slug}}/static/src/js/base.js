const main = document.querySelector('.main');

// Stretch main height to fill the screen
if (main) {
    let footer_height = '';
    let header_height = '';
    if (document.querySelector('.footer')) {
        footer_height = document.querySelector('.footer').offsetHeight;
    } else {
        footer_height = '0';
    }

    if (document.querySelector('.header')) {
        header_height = document.querySelector('.header').offsetHeight;
    } else {
        header_height = '0';
    }
    const total_height = header_height + footer_height;
    main.style.minHeight = `${window.innerHeight - total_height}px`;
}
