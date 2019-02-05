#!/usr/bin/env bash
set -e

WAGTAIL="{{ cookiecutter.wagtail }}"
MULTILINGUAL="{{ cookiecutter.multilingual }}"

if [ "$WAGTAIL" == "y" ]; then
    # Wagtail requested - use the wagtail base HTML file with extra tags
    mv templates/base_wagtail.html templates/base.html
else
    # No wagtail - remove any wagtail related files
    rm -rf apps/pages
    rm -rf apps/settings
    rm -rf templates/blocks
    rm -rf templates/pages
    rm -rf templates/wagtail
    rm -f templates/base_wagtail.html
fi

if [ "$MULTILINGUAL" == "y" ]; then
    
    # create locale directory
    mkdir -p locale/en

    # use the multilingual templates
    mv templates/base_multilingual.html templates/base.html
    mv templates/404_multilingual.html templates/404.html
    mv templates/500_multilingual.html templates/500.html

else
    rm -rf apps/core/tests
    rm -rf templates/base_multilingual.html
    rm -rf templates/404_multilingual.html
    rm -rf templates/500_multilingual.html
fi
