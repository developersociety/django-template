"""
Django settings for {{ cookiecutter.project_slug }} project.

For more information on this file, see
https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/
"""

import os
import sys

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Production / development switches
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/howto/deployment/checklist/

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

# Email
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#email

ADMINS = [("Developer Society", "studio@dev.ngo")]
MANAGERS = ADMINS

SERVER_EMAIL = "{{ cookiecutter.project_slug }}@devsoc.org"
DEFAULT_FROM_EMAIL = "{{ cookiecutter.project_slug }}@devsoc.org"
EMAIL_SUBJECT_PREFIX = "[{{ cookiecutter.project_slug }}] "

PROJECT_APPS_ROOT = os.path.join(BASE_DIR, "apps")
sys.path.append(PROJECT_APPS_ROOT)

DEFAULT_APPS = [
    # These apps should come first to load correctly.
    "core.apps.CoreConfig",
    "django.contrib.admin.apps.AdminConfig",
    "django.contrib.auth.apps.AuthConfig",
    "django.contrib.contenttypes.apps.ContentTypesConfig",
    "django.contrib.sessions.apps.SessionsConfig",
    "django.contrib.messages.apps.MessagesConfig",
    "django.contrib.staticfiles.apps.StaticFilesConfig",
{%- if cookiecutter.wagtail == 'y' %}
    "django.contrib.sitemaps.apps.SiteMapsConfig",
{%- else %}
    "django.contrib.sites.apps.SitesConfig",
{%- endif %}
{%- if cookiecutter.geodjango == 'y' %}
    "django.contrib.gis.apps.GISConfig",
{%- endif %}
]
{%- if cookiecutter.wagtail == 'y' %}

THIRD_PARTY_APPS = [
    "modelcluster",
    "raven.contrib.django.apps.RavenConfig",
    "rest_framework",
    "taggit",
    "wagtail.admin",
    "wagtail.contrib.forms",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.settings",
    "wagtail.core",
    "wagtail.documents",
    "wagtail.embeds",
    "wagtail.images",
    "wagtail.search",
    "wagtail.sites",
    "wagtail.snippets",
    "wagtail.users",
    "wagtailfontawesome",
]
{%- else %}

THIRD_PARTY_APPS = ["raven.contrib.django.apps.RavenConfig"]
{%- endif %}
{%- if cookiecutter.wagtail == 'y' %}

PROJECT_APPS = ["pages", "settings.apps.SettingsConfig"]
{%- else %}

PROJECT_APPS = []
{%- endif %}

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
{%- if cookiecutter.wagtail == 'y' %}
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
{%- else %}
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
{%- endif %}
]

ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"

WSGI_APPLICATION = "{{ cookiecutter.project_slug }}.wsgi.application"

# Database
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#databases

DATABASES = {"default": dj_database_url.config()}

# Caches
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/cache/

CACHES = {}
if os.environ.get("MEMCACHED_SERVERS"):
    CACHES["default"] = {
        "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
        "LOCATION": os.environ["MEMCACHED_SERVERS"].split(" "),
        "KEY_PREFIX": os.environ.get("MEMCACHED_PREFIX"),
    }
else:
    CACHES["default"] = {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}

# Internationalization
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = False

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/howto/static-files/

STATIC_URL = os.environ.get("STATIC_URL", "/static/")

STATIC_ROOT = os.path.join(BASE_DIR, "htdocs/static")

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# File uploads
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#file-uploads

MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")

MEDIA_ROOT = os.path.join(BASE_DIR, "htdocs/media")

DEFAULT_FILE_STORAGE = os.environ.get(
    "DEFAULT_FILE_STORAGE", "django.core.files.storage.FileSystemStorage"
)

# Templates
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.demo",
{%- if cookiecutter.wagtail == 'y' %}
                "wagtail.contrib.settings.context_processors.settings",
{%- endif %}
            ]
        },
    }
]

# Logging
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/logging/#configuring-logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        }
    },
    "root": {"level": "WARNING", "handlers": ["sentry"]},
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
        "sentry": {
            "level": "ERROR",
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "django.db.backends": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "django.server": {"handlers": ["django.server"], "level": "INFO", "propagate": False},
        "elasticapm.errors": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "py.warnings": {"handlers": ["console"]},
        "raven": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "sentry.errors": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
    },
}

# Sites framework
SITE_ID = 1

# Cloud storage
CONTENTFILES_PREFIX = "{{ cookiecutter.project_slug }}"
CONTENTFILES_SSL = True

# Improved cookie security
CSRF_COOKIE_HTTPONLY = True
{%- if cookiecutter.wagtail == 'y' %}

# Wagtail
WAGTAIL_SITE_NAME = "{{ cookiecutter.project_name }}"
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.elasticsearch6",
        "URLS": [os.environ.get("SEARCH_URL", "http://127.0.0.1:9200")],
        "INDEX": os.environ.get("SEARCH_INDEX", "{{ cookiecutter.project_slug }}"),
    }
}
{%- endif %}
{%- if cookiecutter.geodjango == 'y' %}

# GeoDjango fixes
GDAL_LIBRARY_PATH = os.environ.get("GDAL_LIBRARY_PATH")
GEOS_LIBRARY_PATH = os.environ.get("GEOS_LIBRARY_PATH")
{%- endif %}

DEMO_SITE = False
