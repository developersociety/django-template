# -*- coding: utf-8 -*-

from .base import *  # NOQA @UnusedWildImport


ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(' ')


DEBUG = False


TEMPLATE_DEBUG = DEBUG

