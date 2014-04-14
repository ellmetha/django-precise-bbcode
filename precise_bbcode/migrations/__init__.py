# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
# Local application / specific library imports

SOUTH_ERROR_MESSAGE = """\n
To support South migrations, you should customize the SOUTH_MIGRATION_MODULES setting as follow:

    SOUTH_MIGRATION_MODULES = {
        'precise_bbcode': 'precise_bbcode.south_migrations',
    }
"""

# These migrations will work if Django 1.7 or greater is installed
try:
    from django.db import migrations
except ImportError:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(SOUTH_ERROR_MESSAGE)
