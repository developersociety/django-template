document.body.onclick = (event) => {
    const target = event.target;

    if (target.classList.contains('advanced-features-toggle')) {
        const advanced_features = target.nextElementSibling;

        // Toggle show of features
        advanced_features.hidden = !advanced_features.hidden;
    }
};

document.body.onchange = (event) => {
    const target = event.target;

    if (target.id.includes('link_to')) {
        const value = target.value;
        const parent = target.closest('.url-picker');
        const fields = [...parent.children];

        // Remove first element as that refers to selector
        fields.shift();

        // Show field that has been selected above
        fields.forEach((field) => {
            if (
                value !== '' &&
                (field.dataset.field === value ||
                    field.dataset.field === 'link_text' ||
                    field.dataset.field === 'new_window')
            ) {
                field.style.display = 'block';
            } else {
                field.style.display = 'none';
            }
        });
    }
};

window.onload = () => {
    const active_advanced_features = [...document.querySelectorAll('.advanced-features')];

    const active_url_selectors = [...document.querySelectorAll('.url-picker')];

    // If error present in advanced features then show
    active_advanced_features.forEach((feature_set) => {
        if (feature_set.querySelectorAll('.error').length !== 0) {
            feature_set.hidden = false;
        }
    });

    // Show link options if a link has been chosen
    active_url_selectors.forEach((feature_set) => {
        const link_to_type = feature_set.querySelector('select[name*="link_to"').value;

        if (link_to_type !== '') {
            const fields = feature_set.querySelectorAll(
                `li[data-field="${link_to_type}"], li[data-field="new_window"], li[data-field="link_text"]`
            );

            fields.forEach((field) => {
                field.style.display = 'block';
            });
        }
    });
};
