#!/usr/bin/env bash
set -e

WAGTAIL="{{ cookiecutter.wagtail }}"

if [ "$WAGTAIL" == "y" ]; then
    # Wagtail requested - use the wagtail base HTML file with includes and extra tags
    mv templates/base_wagtail.html templates/base.html
    mv templates/includes/footer_wagtail.html templates/includes/footer.html
    mv templates/includes/header_wagtail.html templates/includes/header.html
    mv templates/includes/social_wagtail.html templates/includes/social.html
else
    # No wagtail - remove any wagtail related files
    rm -f apps/core/wagtail_hooks.py
    rm -f static/src/js/admin.js
    rm -f static/src/scss/admin_styles.scss
    rm -rf apps/base
    rm -rf apps/contact
    rm -rf apps/pages
    rm -rf apps/settings
    rm -rf templates/admin
    rm -rf templates/blocks
    rm -rf templates/contact
    rm -rf templates/includes/navigation_tags
    rm -rf templates/pages
    rm -rf templates/wagtailadmin
    rm -f templates/base_wagtail.html
    rm -f templates/includes/footer_wagtail.html
    rm -f templates/includes/header_wagtail.html
    rm -f templates/includes/social_wagtail.html
fi
