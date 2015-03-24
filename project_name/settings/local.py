# -*- coding: utf-8 -*-

from .base import *  # NOQA @UnusedWildImport

DEBUG = True


TEMPALTE_DEBUG = DEBUG


INTERNAL_IPS = (
    '127.0.0.1',
)


INSTALLED_APPS.append(
    'debug_toolbar',
)


MIDDLEWARE_CLASSES.append(
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

COVERAGE_EXCLUDES_FOLDERS = ['/var/envs/{{ project_name }}/lib/python2']

