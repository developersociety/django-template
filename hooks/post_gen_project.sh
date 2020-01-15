#!/usr/bin/env bash
set -e

WAGTAIL="{{ cookiecutter.wagtail }}"
MULTILINGUAL="{{ cookiecutter.multilingual }}"

if [ "$WAGTAIL" == "y" ] && [ "$MULTILINGUAL" == "y" ]; then
    # Wagtail requested with multilingual features

    # use multilingual wagtail base
    mv apps/core/views_wagtail.py apps/core/views.py
    mv templates/base_wagtail_multilingual.html templates/base.html
    mv templates/404_multilingual.html templates/404.html
    mv templates/500_multilingual.html templates/500.html
    mv templates/includes/social_wagtail.html templates/includes/social.html

    # remove unused base templates
    rm -f templates/base_multilingual.html
    rm -f templates/base_wagtail_multilingual.html
    rm -f templates/base_wagtail.html
    rm -f templates/404_multilingual.html
    rm -f templates/500_multilingual.html

    # remove irrelevant tests
    rm -rf apps/core/tests

elif [ "$WAGTAIL" == "y" ] && [ "$MULTILINGUAL" == "n" ]; then
    # Wagtail requested
    mv apps/core/views_wagtail.py apps/core/views.py

    # Wagtail requested - use the wagtail base HTML file with extra tags
    mv templates/base_wagtail.html templates/base.html
    mv templates/includes/meta_wagtail.html templates/includes/meta.html
    mv templates/includes/social_wagtail.html templates/includes/social.html

    # And remove non-wagtail templates
    rm -f templates/homepage.html
    rm -f templates/base_multilingual.html
    rm -f templates/base_wagtail_multilingual.html
    rm -f templates/base_wagtail.html
    rm -f templates/404_multilingual.html
    rm -f templates/500_multilingual.html

    # remove multilingual files
    rm -rf apps/core/tests
    rm -f templates/base_multilingual.html

    # remove the lanuage redirect
    rm -rf apps/pages/views.py

elif [ "$WAGTAIL" == "n" ] && [ "$MULTILINGUAL" == "y" ]; then
    # Standard django project with multilingual features (no wagtail)

    # create locale directory
    mkdir -p locale

    # use the multilingual templates
    mv templates/base_multilingual.html templates/base.html
    mv templates/404_multilingual.html templates/404.html
    mv templates/500_multilingual.html templates/500.html

    # remove any wagtail related files
    # No wagtail - remove any wagtail related files
    rm -f apps/core/monkeypatch.py
    rm -f apps/core/views_wagtail.py
    rm -f apps/core/widgets.py
    rm -f apps/core/wagtail_hooks.py
    rm -f apps/core/urls.py
    rm -f static/src/js/admin.js
    rm -f static/src/scss/admin.scss
    rm -rf apps/images
    rm -rf apps/pages
    rm -rf apps/settings
    rm -rf templates/admin
    rm -rf templates/blocks
    rm -rf templates/pages
    rm -rf templates/wagtail
    rm -rf templates/wagtailadmin
    rm -f templates/base_wagtail.html
    rm -f templates/base_multilingual.html
    rm -f templates/base_wagtail_multilingual.html
    rm -f templates/base_wagtail.html
    rm -f templates/includes/meta_wagtail.html
    rm -f templates/includes/social_wagtail.html
    rm -f templates/404_multilingual.html
    rm -f templates/500_multilingual.html

else
    # remove multilingual files
    rm -rf apps/core/tests
    rm -f templates/base_multilingual.html
    rm -f templates/base_wagtail_multilingual.html
    rm -f templates/base_wagtail.html
    rm -f templates/404_multilingual.html
    rm -f templates/500_multilingual.html


    # No wagtail - remove any wagtail related files
    rm -f apps/core/monkeypatch.py
    rm -f apps/core/views_wagtail.py
    rm -f apps/core/widgets.py
    rm -f apps/core/wagtail_hooks.py
    rm -f apps/core/urls.py
    rm -f static/src/js/admin.js
    rm -f static/src/scss/admin.scss
    rm -rf apps/images
    rm -rf apps/pages
    rm -rf apps/settings
    rm -rf templates/admin
    rm -rf templates/blocks
    rm -rf templates/pages
    rm -rf templates/wagtail
    rm -rf templates/wagtailadmin
    rm -f templates/includes/meta_wagtail.html
    rm -f templates/includes/social_wagtail.html

fi