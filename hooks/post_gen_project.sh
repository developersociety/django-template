#!/usr/bin/env bash
set -e

WAGTAIL="{{ cookiecutter.wagtail }}"

if [ "$WAGTAIL" == "y" ]; then
    # Wagtail requested - use wagtail files and remove static fallbacks
    mv templates/base_wagtail.html templates/base.html
    mv templates/includes/meta_wagtail.html templates/includes/meta.html
    mv ./wagtail_webpack.config.js ./webpack.config.js
    mv static/src/scss/blocks/_blocks_wagtail.scss static/src/scss/blocks/_blocks.scss
    rm -f templates/homepage.html
else
    # No wagtail - remove all wagtail related files
    rm -f apps/core/monkeypatch.py
    rm -f apps/core/wagtail_hooks.py
    rm -rf apps/pages
    rm -rf apps/settings
    rm -rf templates/admin
    rm -rf templates/blocks
    rm -rf templates/pages
    rm -rf templates/wagtail
    rm -f templates/base_wagtail.html
    rm -f templates/includes/meta_wagtail.html
    rm -r static/src/js/admin.js
    rm -r ./wagtail_webpack.config.js
    rm -r static/src/scss/blocks/_blocks_wagtail.scss
    rm -r static/src/scss/blocks/_image.scss
    rm -r static/src/scss/blocks/_richtext.scss
    rm -r static/src/scss/blocks/_two_column.scss
fi
