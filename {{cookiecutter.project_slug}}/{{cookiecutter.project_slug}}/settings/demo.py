import os

from .production import *  # noqa

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEMO_SITE = True or 'DEMO_SITE' in os.environ
