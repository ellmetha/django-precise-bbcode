# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


# python_2_unicode_compatible
try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError:
    python_2_unicode_compatible = lambda x: x

# force_str
try:
    from django.utils.encoding import force_str
except ImportError:
    from django.utils.encoding import smart_str as force_str  # noqa


# get_model
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models import get_model  # noqa


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    class metaclass(meta):  # noqa
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass("NewBase", None, {})
