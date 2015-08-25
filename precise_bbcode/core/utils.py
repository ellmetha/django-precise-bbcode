# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from functools import reduce


def replace(data, replacements):
    """
    Performs several string substitutions on the initial ``data`` string using
    a list of 2-tuples (old, new) defining substitutions and returns the resulting
    string.
    """
    return reduce(lambda a, kv: a.replace(*kv), replacements, data)
