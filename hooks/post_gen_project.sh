#!/usr/bin/env bash
set -e

WAGTAIL="{{ cookiecutter.wagtail }}"
MULTILINGUAL="{{ cookiecutter.multilingual }}"

if [ "$WAGTAIL" == "y" ] && [ "$MULTILINGUAL" == "y" ]; then
    # Wagtail requested with multilingual features
    
    # use multilingual wagtail base
    mv templates/base_wagtail_multilingual.html templates/base.html

    # use the multilingual 500/404 templates
    mv templates/404_multilingual.html templates/404.html
    mv templates/500_multilingual.html templates/500.html

    # remove unused base templates
    rm -rf templates/base_multilingual.html
    rm -rf templates/base_wagtail.html

    # remove irrelevant tests
    rm -rf apps/core/tests

elif [ "$WAGTAIL" == "y" ] && [ "$MULTILINGUAL" == "n" ]; then
    # Wagtail requested with no multilingual features

    # use standard wagtail base template
    mv templates/base_wagtail.html templates/base.html

    # remove multilingual files
    rm -rf apps/core/tests
    rm -rf templates/base_multilingual.html
    rm -rf templates/404_multilingual.html
    rm -rf templates/500_multilingual.html

elif [ "$WAGTAIL" == "n" ] && [ "$MULTILINGUAL" == "y" ]; then
    # Standard django project with multilingual features (no wagtail)

    # create local directory
    mkdir -p locale/en

    # use the multilingual templates
    mv templates/base_multilingual.html templates/base.html
    mv templates/404_multilingual.html templates/404.html
    mv templates/500_multilingual.html templates/500.html

    # remove any wagtail related files
    rm -rf apps/pages
    rm -rf apps/settings
    rm -rf templates/blocks
    rm -rf templates/pages
    rm -rf templates/wagtail
    rm -f templates/base_wagtail.html

else
    # Neither wagtail or multilingual project

    # remove multilingual files
    rm -rf apps/core/tests
    rm -rf templates/base_multilingual.html
    rm -rf templates/404_multilingual.html
    rm -rf templates/500_multilingual.html

    # remove any wagtail related files
    rm -rf apps/pages
    rm -rf apps/settings
    rm -rf templates/blocks
    rm -rf templates/pages
    rm -rf templates/wagtail
    rm -f templates/base_wagtail.html

    # remove multilingual wagtail base
    rm -rf templates/base_wagtail_multilingual.html

fi