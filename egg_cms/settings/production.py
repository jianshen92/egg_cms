from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

SITE_URL = 'http://cms.egg.network'

try:
    from .local import *
except ImportError:
    pass
