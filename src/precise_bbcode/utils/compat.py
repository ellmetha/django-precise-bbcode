# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
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
