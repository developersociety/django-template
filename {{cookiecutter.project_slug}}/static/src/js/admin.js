document.body.onclick = (event) => {
    const target = event.target;

    if (target.classList.contains('collapse-expand-block')) {
        const header = target.closest('.admin-block-header');
        const fields = header.nextElementSibling;

        // Toggle show of features
        fields.classList.toggle('collapsed');
    }
};

document.body.onchange = (event) => {
    const target = event.target;

    if (target.id.includes('link_to')) {
        const value = target.value;
        const parent = target.closest('.url-picker');
        const fields = [
            ...parent.querySelectorAll(`
                li[data-field=page],
                li[data-field=custom_url],
                li[data-field=file]
            `)
        ];

        // Show field that has been selected above
        fields.forEach((field) => {
            if (value !== '' && field.dataset.field === value) {
                field.style.display = 'block';
            } else {
                field.style.display = 'none';
            }
        });
    }
};

window.onload = () => {
    const active_url_selectors = [...document.querySelectorAll('.url-picker')];
    // Show link options if a link has been chosen
    active_url_selectors.forEach((feature_set) => {
        const link_to_type = feature_set.querySelector('select[name*="link_to"').value;

        if (link_to_type !== '') {
            const field = feature_set.querySelector(`li[data-field="${link_to_type}"]`);

            field.style.display = 'block';
        }
    });
};
