# -*- coding: utf-8 -*-

# Standard library imports
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
# Third party imports
try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError:
    python_2_unicode_compatible = lambda x: x

try:
    from django.utils.six import string_types
except ImportError:
    if PY3:
        string_types = str,
    else:
        string_types = basestring,
# Local application / specific library imports


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass("NewBase", None, {})
