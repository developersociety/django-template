"""
Django settings - Django {{ cookiecutter.django_version }}.

For more information on this file, see
https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/
"""

import os
import sys
from datetime import timedelta
from pathlib import Path

from django.db.models.fields import BLANK_CHOICE_DASH
{%- if cookiecutter.multilingual == 'y' %}
from django.utils.translation import gettext_lazy as _
{%- endif %}

import dj_database_url

# The unique project name in slug form
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Production / development switches
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/howto/deployment/checklist/

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

# Email
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#email

ADMINS = [("Developer Society", "studio@dev.ngo")]
MANAGERS = ADMINS

SERVER_EMAIL = os.environ.get("SERVER_EMAIL", f"{PROJECT_SLUG}@devemail.org")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", f"{PROJECT_SLUG}@devemail.org")
EMAIL_SUBJECT_PREFIX = f"[{PROJECT_SLUG}] "

PROJECT_APPS_ROOT = BASE_DIR / "apps"
sys.path.append(PROJECT_APPS_ROOT.as_posix())

DEFAULT_APPS = [
    # These apps should come first to load correctly.
    "core.apps.CoreConfig",
    "django.contrib.admin.apps.AdminConfig",
    "django.contrib.auth.apps.AuthConfig",
    "django.contrib.contenttypes.apps.ContentTypesConfig",
    "django.contrib.sessions.apps.SessionsConfig",
    "django.contrib.messages.apps.MessagesConfig",
    "django.contrib.staticfiles.apps.StaticFilesConfig",
    "django.contrib.sites.apps.SitesConfig",
{%- if cookiecutter.geodjango == 'y' %}
    "django.contrib.gis.apps.GISConfig",
{%- endif %}
]
THIRD_PARTY_APPS = [
    "axes",
    "maskpostgresdata",
    "watchman",
]

PROJECT_APPS = [
    "accounts.apps.AccountsConfig",
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
{%- if cookiecutter.multilingual == 'y' %}
    "django.middleware.locale.LocaleMiddleware",
{%- endif %}
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "project.urls"

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#databases

DATABASES = {}
if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config()

# Caches
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/cache/

CACHES = {}
if os.environ.get("REDIS_SERVERS"):
    CACHES["default"] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ["REDIS_SERVERS"].split(" "),
        "KEY_PREFIX": "{}:cache".format(os.environ["REDIS_PREFIX"]),
    }
else:
    CACHES["default"] = {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}

# Internationalization
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

{%- if cookiecutter.multilingual == 'y' %}

USE_I18N = True
{%- else %}

USE_I18N = False
{%- endif %}

USE_TZ = True

{%- if cookiecutter.multilingual == 'y' %}

# Allowed languages
LANGUAGES = [("en", _("English")), ("uni", _("Unicode Test"))]

LOCALE_PATHS = [BASE_DIR / "locale"]
{%- endif %}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/howto/static-files/

STATIC_URL = os.environ.get("STATIC_URL", "static/")

STATIC_ROOT = BASE_DIR / "htdocs/static"

STATICFILES_DIRS = [BASE_DIR / "static"]

# File uploads
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#file-uploads

MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")

MEDIA_ROOT = BASE_DIR / "htdocs/media"

STORAGES = {
    "default": {
        "BACKEND": os.environ.get(
            "DEFAULT_FILE_STORAGE", "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Templates
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.demo",
                "core.context_processors.sentry_config",
            ]
        },
    }
]

# Replace default value in select fields with empty spaces for a more modern look
BLANK_CHOICE_DASH[0] = ("", " ")

# Logging
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/logging/#configuring-logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "formatter": "django.server",
            "class": "logging.StreamHandler",
        },
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "django.server": {"handlers": ["django.server"], "level": "INFO", "propagate": False},
        "py.warnings": {"handlers": ["console"]},
    },
}

# Sites framework
SITE_ID = 1

# Cloud storage
CONTENTFILES_PREFIX = os.environ.get("CONTENTFILES_PREFIX", f"{PROJECT_SLUG}")
CONTENTFILES_HOSTNAME = os.environ.get("CONTENTFILES_HOSTNAME")
CONTENTFILES_S3_REGION = os.environ.get("CONTENTFILES_S3_REGION")
CONTENTFILES_S3_ENDPOINT_URL = os.environ.get("CONTENTFILES_S3_ENDPOINT_URL")

# Improved cookie security
CSRF_COOKIE_HTTPONLY = True

# Improved login security with axes
# - Only lock attempts by username (prevent mass attempts on single accounts)
# - 10 failures in 5 minutes results in blocking
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "django.contrib.auth.backends.ModelBackend",
]
AXES_LOCKOUT_PARAMETERS = ["username"]
AXES_FAILURE_LIMIT = 10
AXES_COOLOFF_TIME = timedelta(minutes=5)
AXES_ENABLE_ADMIN = False
AXES_SENSITIVE_PARAMETERS = []
{%- if cookiecutter.geodjango == 'y' %}

# GeoDjango fixes
GDAL_LIBRARY_PATH = os.environ.get("GDAL_LIBRARY_PATH")
GEOS_LIBRARY_PATH = os.environ.get("GEOS_LIBRARY_PATH")
{%- endif %}

DEMO_SITE = False

# Health checks
WATCHMAN_CHECKS = [
    "watchman.checks.caches",
    "watchman.checks.databases",
]
WATCHMAN_CACHES = ["default"]  # Avoid additional cache backend hits

# Sentry frontend tracking
SENTRY_JS_URL = os.environ.get("SENTRY_JS_URL")
SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT")
SENTRY_RELEASE = None

AUTH_USER_MODEL = "accounts.User"
