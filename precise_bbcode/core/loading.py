import importlib
import inspect

from django.apps import apps


def get_module(app, modname):
    """
    Internal function to load a module from a single app.
    """
    # Check if the module exists.
    if importlib.util.find_spec('{}.{}'.format(app, modname)) is None:
        return

    # Import the app's module file
    importlib.import_module('{}.{}'.format(app, modname))


def load(modname):
    """
    Loads all modules with name 'modname' from all installed apps.
    """
    app_names = [app.name for app in apps.app_configs.values()]
    for app in app_names:
        get_module(app, modname)


def get_subclasses(mod, cls):
    """
    Yield the classes in module 'mod' that inherit from 'cls'.
    """
    for name, obj in inspect.getmembers(mod):
        if obj != cls and inspect.isclass(obj) and issubclass(obj, cls):
            yield obj
