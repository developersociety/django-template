#!/usr/bin/env bash
set -e

GEODJANGO="{{ cookiecutter.geodjango }}"
WAGTAIL="{{ cookiecutter.wagtail }}"
MULTILINGUAL="{{ cookiecutter.multilingual }}"

if [ "$GEODJANGO" == "y" ]; then
    mv .github/workflows/ci_geodjango.yml .github/workflows/ci.yml
    rm .github/workflows/ci_standard.yml
else
    mv .github/workflows/ci_standard.yml .github/workflows/ci.yml
    rm .github/workflows/ci_geodjango.yml
fi

if [ "$WAGTAIL" == "y" ]; then
    # Use the wagtail base HTML file with extra tags
    mv templates/base_wagtail.html templates/base.html
    mv templates/includes/meta_wagtail.html templates/includes/meta.html

    # And remove non-wagtail templates
    rm -f templates/homepage.html
else
    # Remove wagtail templates
    rm -f apps/core/edit_handlers.py
    rm -rf apps/pages
    rm -rf apps/settings
    rm -rf templates/blocks
    rm -rf templates/pages
    rm -rf templates/wagtail
    rm -f templates/base_wagtail.html
    rm -f templates/includes/meta_wagtail.html
fi

if [ "$MULTILINGUAL" == "y" ]; then
    # Create locale directory
    mkdir -p locale
else
    # Remove multilingual features
    rm -f apps/pages/views.py
    rm -rf apps/core/tests
fi
