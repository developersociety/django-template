from .production import *  # noqa

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEMO_SITE = True

# Wagtail site name is used for 2FA, so give the demo site a unique name
WAGTAIL_SITE_NAME = f"{WAGTAIL_SITE_NAME} (demo)"
