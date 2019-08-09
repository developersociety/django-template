/* global $ */
// This file contains logic to support custom wagtail admin styles and templates

// Expand / collapse advanced features blocks
document.body.onclick = (event) => {
    const target = event.target;

    if (target.classList.contains('advanced-features-toggle')) {
        const advanced_features = target.nextElementSibling;

        // Toggle show of features
        advanced_features.hidden = !advanced_features.hidden;
    }

    if (target.classList.contains('collapse-expand-block')) {
        const header = target.closest('.block-header');
        const fields = header.nextElementSibling;

        // Toggle show of features
        fields.classList.toggle('collapsed');
    }
};

// Listen for link_to field changes on LinkBlock, and show selected page OR file OR custom_url field
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

        // Show selected field only
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
    const active_advanced_features = [...document.querySelectorAll('.advanced-features')];
    const active_url_selectors = [...document.querySelectorAll('.url-picker')];
    const structure_form = document.getElementById('structure_form');

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
            const field = feature_set.querySelector(`li[data-field="${link_to_type}"]`);

            field.style.display = 'block';
        }
    });
    if (structure_form != null) {
        structure_form.onsubmit = () => {
            $('body > .modal').remove();
            // set default contents of container
            const container = `
                <div class="modal fade in" tabindex="-1" role="dialog" aria-hidden="true" style="display: block">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-body">
                                <header class="merged tab-merged ">
                                    <div class="row nice-padding">
                                        <div class="left">
                                            <div class="col header-title">
                                                <h1 class="icon icon-spinner">
                                                Submitting Data</h1>
                                            </div>

                                        </div>
                                    </div>
                                </header>
                                <div class="tab-content">
                                    <section class="active">
                                        <div class="nice-padding">
                                            <p>This process may take up to one minute.</p>
                                        </div>
                                    </section>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-backdrop fade in"></div>
            `;
            $('body').append(container);
            $('body').addClass('modal-open');
        };
    }
};
