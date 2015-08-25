# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class InvalidBBCodeTag(Exception):
    """The bbcode tag is not valid and cannot be used."""
    pass


class InvalidBBCodePlaholder(Exception):
    """The placeholder is not valid and cannot be used."""
    pass
