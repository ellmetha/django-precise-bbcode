# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import imp
import inspect

# Third party imports
from django.conf import settings
from django.utils.importlib import import_module

# Local application / specific library imports


def get_module(app, modname):
    """
    Internal function to load a module from a single app.
    """
    # Find out the app's __path__
    try:
        app_path = import_module(app).__path__
    except AttributeError:
        return

    # Use imp.find_module to find the app's modname.py
    try:
        imp.find_module(modname, app_path)
    except ImportError:
        return

    # Import the app's module file
    import_module('{}.{}'.format(app, modname))


def load(modname):
    """
    Loads all modules with name 'modname' from all installed apps.
    """
    for app in settings.INSTALLED_APPS:
        get_module(app, modname)


def get_subclasses(mod, cls):
    """
    Yield the classes in module 'mod' that inherit from 'cls'.
    """
    for name, obj in inspect.getmembers(mod):
        if obj != cls and inspect.isclass(obj) and issubclass(obj, cls):
            yield obj
