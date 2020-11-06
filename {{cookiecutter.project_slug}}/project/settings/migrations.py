from .base import *  # noqa

{%- if cookiecutter.wagtail == 'y' %}

# makemigrations --check requires a database starting with Wagtail 2.10, but we don't want to try
# connecting to a real one - so use an in-memory sqlite one.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
{%- else %}

# makemigrations --check requires a database if DATABASES is populated, but works fine without, so
# we set this to an empty dict to stop makemigrations connecting to a database which doesn't exist
DATABASES = {}
{%- endif %}

SECRET_KEY = "secret"
