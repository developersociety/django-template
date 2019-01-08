const image_grids = [...document.querySelectorAll('.image-grid-block')];

image_grids.forEach((grid) => {
    const cells = [...grid.querySelectorAll('.image-grid__cell')];
    const lightbox = grid.querySelector('.image-grid__lightbox');
    const lightbox_append = grid.querySelector('.image-grid__lightbox-append');
    const lightbox_close = grid.querySelector('.image-grid__lightbox-close');

    cells.forEach((cell) => {
        cell.onclick = () => {
            const image_url = cell.dataset.image;
            const caption_text = cell.textContent;
            const image = document.createElement('img');
            const caption = document.createElement('p');

            image.src = image_url;
            caption.textContent = caption_text;

            // Fade in lightbox and display image
            document.body.style.overflow = 'hidden';
            lightbox_append.appendChild(image);
            lightbox_append.appendChild(caption);
            lightbox.style.display = 'flex';
        };
    });

    lightbox.onclick = (event) => {
        // if clicked away hide lightbox
        if (event.target === lightbox || event.target === lightbox_close) {
            document.body.style.overflow = 'auto';
            lightbox.style.display = 'none';

            // Remove children for re-render
            while (lightbox_append.firstChild) {
                lightbox_append.firstChild.remove();
            }
        }
    };
});
