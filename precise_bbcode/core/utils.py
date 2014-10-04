# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals

# Third party imports
# Local application / specific library imports


def replace(data, replacements):
    """
    Given a list of 2-tuples (old, new), performs all replacements on the data and
    returns the result.
    """
    for old, new in replacements:
        data = data.replace(old, new)
    return data
