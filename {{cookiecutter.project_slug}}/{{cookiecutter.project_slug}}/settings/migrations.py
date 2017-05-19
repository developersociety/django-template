from .base import *  # noqa

# makemigrations --check requires a database if DATABASES is populated, but works fine without, so
# we set this to an empty dict to stop makemigrations connecting to a database which doesn't exist
DATABASES = {}

SECRET_KEY = '{{ cookiecutter.project_slug }}'
