#!/usr/bin/env bash
set -e

GLITTER="{{ cookiecutter.glitter }}"

if [ "$GLITTER" == "y" ]; then
    # Glitter requested - use the glitter base HTML file with extra tags
    mv templates/base_glitter.html templates/base.html
else
    # No glitter - remove any glitter related files
    rm -rf apps/pages
    rm -rf templates/glitter
    rm -f templates/base_glitter.html
fi
