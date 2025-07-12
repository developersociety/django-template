# ruff: noqa:F405
import os

from .production import *  # noqa:F403

DEMO_SITE = True

# Intercept outgoing emails
INSTALLED_APPS = [*INSTALLED_APPS, "bandit"]
BANDIT_EMAIL = os.environ.get("BANDIT_EMAIL", "").split(" ")
EMAIL_SUBJECT_PREFIX = f"[{PROJECT_SLUG} demo] "
EMAIL_BACKEND = "bandit.backends.smtp.HijackSMTPBackend"
BANDIT_REGEX_WHITELIST = [
    r"(?i)^.+@dev\.ngo$",
]
