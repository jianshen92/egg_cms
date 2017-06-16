from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h+r3+ok+olvh8l)8ha$=+#zg!j*icmbr4##x9kj(zarz@+*l5p'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_URL = 'http://127.0.0.1:8000'

try:
    from .local import *
except ImportError:
    pass
