import os

from .base import *  # noqa

DEBUG = True
TEMPLATES[0]["OPTIONS"]["debug"] = True

DATABASES = {
    "default": {
{%- if cookiecutter.geodjango == 'y' %}
        "ENGINE": "django.contrib.gis.db.backends.postgis",
{%- else %}
        "ENGINE": "django.db.backends.postgresql_psycopg2",
{%- endif %}
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", "{{ cookiecutter.project_slug }}_django"),
        "USER": "",
        "PASSWORD": "",
        "PORT": "",
    }
}

INTERNAL_IPS = ["127.0.0.1"]
ALLOWED_HOSTS = ["*"]

{%- if cookiecutter.wagtail == 'y' %}
INSTALLED_APPS += ["django_extensions", "wagtail.contrib.styleguide"]
{%- else %}
INSTALLED_APPS += ["django_extensions"]
{%- endif %}

# Webpack runserver
TEMPLATES[0]["OPTIONS"]["context_processors"].append("core.context_processors.browsersync")

# Use vanilla StaticFilesStorage to allow tests to run outside of tox easily
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

SECRET_KEY = "secret"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Django debug toolbar - show locally unless DISABLE_TOOLBAR is enabled with environment vars
# eg. DISABLE_TOOLBAR=1 ./manage.py runserver
if not os.environ.get("DISABLE_TOOLBAR"):
    INSTALLED_APPS += ["debug_toolbar"]

    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

# Allow login with remote passwords, but downgrade/swap to crypt for password hashing speed
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.CryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]
{%- if cookiecutter.wagtail == 'y' %}

# Wagtail search - use Postgres unless ENABLE_ELASTICSEARCH is enabled with environment vars
# eg. ENABLE_ELASTICSEARCH=1 ./manage.py runserver
if not os.environ.get("ENABLE_ELASTICSEARCH"):
    INSTALLED_APPS += ["wagtail.contrib.postgres_search"]

    WAGTAILSEARCH_BACKENDS = {"default": {"BACKEND": "wagtail.contrib.postgres_search.backend"}}
{%- endif %}
