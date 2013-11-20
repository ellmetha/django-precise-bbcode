# Standard library imports
import sys

# Third party imports
# Local application / specific library imports
from .dev import *


if 'test' in sys.argv:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', }, }
    SOUTH_TESTS_MIGRATE = False  # To disable migrations and use syncdb instead
    SKIP_SOUTH_TESTS = True  # To disable South's own unit tests
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ma_ep_precisebbcode',
            'USER': 'ma',
            'PASSWORD': 'myr_1adISh3re',
            'HOST': '',
            'PORT': '',
        }
    }
