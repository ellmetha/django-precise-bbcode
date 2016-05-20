# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os

from django.conf import settings


TEST_ROOT = os.path.abspath(os.path.dirname(__file__))


DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [],
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ),
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'APP_DIRS': True,
        'DIRS': [],
        'OPTIONS': {
            'extensions': [
                'precise_bbcode.jinja2tags.bbcode',
            ],
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'precise_bbcode',
    'tests',
    'django.contrib.admin',
)

ROOT_URLCONF = 'tests._testsite.urls'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ADMINS = ('admin@example.com',)

MEDIA_ROOT = os.path.join(TEST_ROOT, '_testdata/media/')

SITE_ID = 1

# Setting this explicitly prevents Django 1.7+ from showing a
# warning regarding a changed default test runner. The test
# suite is run with py.test, so it does not matter.
SILENCED_SYSTEM_CHECKS = ['1_6.W001']

SECRET_KEY = 'key'
