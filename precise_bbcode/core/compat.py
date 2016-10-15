# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


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
