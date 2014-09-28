# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
from collections import defaultdict
import re

# Third party imports
from django.db.models import get_model
from django.utils.encoding import python_2_unicode_compatible

# Local application / specific library imports
from precise_bbcode.conf import settings as bbcode_settings


_bbcode_parser = None
# The easiest way to use the BBcode parser is to import the following get_parser function (except if
# you need many BBCodeParser instances at a time or you want to subclass it).
# 
# Note if you create a new instance of BBCodeParser, the built in bbcode tags are still installed.


def get_parser():
    if not _bbcode_parser:
        _load_parser()
    return _bbcode_parser


def _init_bbcode_tags(parser):
    """
    Call the BBCode tag pool to fetch all the module-based tags and initializes
    their associated renderers.
    """
    from precise_bbcode.tag_pool import tag_pool
    tags = tag_pool.get_tags()
    for tag_def in tags:
        tag = tag_def()
        parser.add_renderer(tag.tag_name, tag.render, **tag._options())


def _init_custom_bbcode_tags(parser):
    """
    Find the user-defined BBCode tags and initializes their associated renderers.
    """
    BBCodeTag = get_model('precise_bbcode', 'BBCodeTag')
    if BBCodeTag:
        custom_tags = BBCodeTag.objects.all()
        for tag in custom_tags:
            args, kwargs = tag.parser_args
            parser.add_default_renderer(*args, **kwargs)


def _init_bbcode_smilies(parser):
    """
    Find the user-defined smilies tags and register them to the BBCode parser.
    """
    SmileyTag = get_model('precise_bbcode', 'SmileyTag')
    if SmileyTag:
        custom_smilies = SmileyTag.objects.all()
        for smiley in custom_smilies:
            parser.add_smiley(smiley.code, smiley.html_code)


def _load_parser():
    global _bbcode_parser
    _bbcode_parser = BBCodeParser()

    # Init renderers registered in 'bbcode_tags' modules
    _init_bbcode_tags(_bbcode_parser)

    # Init custom renderers defined in BBCodeTag model instances
    if bbcode_settings.BBCODE_ALLOW_CUSTOM_TAGS:
        _init_custom_bbcode_tags(_bbcode_parser)

    # Init smilies
    if bbcode_settings.BBCODE_ALLOW_SMILIES:
        _init_bbcode_smilies(_bbcode_parser)


from .parser import *
