#!/usr/bin/env bash
set -e

GEODJANGO="{{ cookiecutter.geodjango }}"
MULTILINGUAL="{{ cookiecutter.multilingual }}"

if [ "$GEODJANGO" == "y" ]; then
    mv .github/workflows/ci_geodjango.yml .github/workflows/ci.yml
    rm .github/workflows/ci_standard.yml
else
    mv .github/workflows/ci_standard.yml .github/workflows/ci.yml
    rm .github/workflows/ci_geodjango.yml
fi

if [ "$MULTILINGUAL" == "y" ]; then
    # Create locale directory
    mkdir -p locale
else
    # Remove multilingual features
    rm -f apps/pages/views.py
    rm -rf apps/core/tests
fi
