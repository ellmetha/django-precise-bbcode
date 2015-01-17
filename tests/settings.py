# -*- coding: utf-8 -*-

# Standard library imports
import os

# Third party imports
from django.conf import global_settings as default_settings
from django.conf import settings

# Local application / specific library imports


TEST_ROOT = os.path.abspath(os.path.dirname(__file__))


TEST_SETTINGS = {
    'DEBUG': False,
    'TEMPLATE_DEBUG': False,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    'TEMPLATE_CONTEXT_PROCESSORS': default_settings.TEMPLATE_CONTEXT_PROCESSORS,
    'INSTALLED_APPS': (
        'django.contrib.auth',
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.sites',
        'precise_bbcode',
        'tests',
    ),
    'ROOT_URLCONF': 'tests._testsite.urls',
    'MIDDLEWARE_CLASSES': default_settings.MIDDLEWARE_CLASSES,
    'ADMINS': ('admin@example.com',),
    'MEDIA_ROOT': os.path.join(TEST_ROOT, '_testdata/media/'),
    'SITE_ID': 1,


    # Setting this explicitly prevents Django 1.7+ from showing a
    # warning regarding a changed default test runner. The test
    # suite is run with nose, so it does not matter.
    'SILENCED_SYSTEM_CHECKS': ['1_6.W001'],
}


def configure():
    if not settings.configured:
        settings.configure(**TEST_SETTINGS)
