#! /usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

COOKIECUTTER_DIR=$1
COOKIECUTTER_ARGS=( "${@:2}" )
TEST_DIR=$(mktemp -d)
cookiecutter --no-input -o "$TEST_DIR" "$COOKIECUTTER_DIR" "${COOKIECUTTER_ARGS[@]}"
pushd "$TEST_DIR/projectname"
tox
popd
rm -rf "$TEST_DIR"
