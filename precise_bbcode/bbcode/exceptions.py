# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals

# Third party imports
# Local application / specific library imports


class InvalidBBCodeTag(Exception):
    """The bbcode tag is not valid and cannot be used."""
    pass


class InvalidBBCodePlaholder(Exception):
    """The placeholder is not valid and cannot be used."""
    pass
