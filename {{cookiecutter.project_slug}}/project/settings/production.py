import os
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger

from .base import *  # noqa

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")

DEBUG = False

# Persistent database connections
if os.environ.get("DATABASE_CONN_MAX_AGE"):
    DATABASES["default"]["CONN_MAX_AGE"] = int(os.environ.get("DATABASE_CONN_MAX_AGE"))

# Avoid server side cursors with pgbouncer
if os.environ.get("DATABASE_PGBOUNCER"):
    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True

# Use cached templates in production
TEMPLATES[0]["APP_DIRS"] = False
TEMPLATES[0]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# SSL required for session/CSRF cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Improve password security to a reasonable bare minimum
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Add more raven data to help diagnose bugs
try:
    SENTRY_RELEASE = (Path(BASE_DIR) / Path(".sentry-release")).read_text().strip()
except FileNotFoundError:
    SENTRY_RELEASE = None

sentry_sdk.init(release=SENTRY_RELEASE, integrations=[DjangoIntegration()])

for logger in ["elasticapm.errors", "elasticapm.transport", "elasticapm.transport.http"]:
    ignore_logger(logger)

# Elastic APM
if os.environ.get("ELASTIC_APM_SERVER_URL"):
    INSTALLED_APPS += ["elasticapm.contrib.django.apps.ElasticAPMConfig"]

    MIDDLEWARE = ["elasticapm.contrib.django.middleware.TracingMiddleware"] + MIDDLEWARE

# Cache sessions for optimum performance
if os.environ.get("REDIS_SERVERS"):
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
{%- if cookiecutter.wagtail == 'y' %}

# For convenience, 2FA is optional - this is False by default for most sites
# If this is True, then 2FA is required for staff users (but this will not impact end users)
WAGTAIL_2FA_REQUIRED = False
{%- endif %}
