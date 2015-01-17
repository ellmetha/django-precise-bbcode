# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals

# Third party imports
from django.db.models import get_model

# Local application / specific library imports
from .parser import BBCodeParser
from .placeholder import BBCodePlaceholder
from .tag import BBCodeTag
from precise_bbcode.conf import settings as bbcode_settings
from precise_bbcode.core.loading import get_subclasses


_bbcode_parser = None
# The easiest way to use the BBcode parser is to import the following get_parser function (except if
# you need many BBCodeParser instances at a time or you want to subclass it).
# Note if you create a new instance of BBCodeParser, the built in bbcode tags will not be installed.


def get_parser():
    if not _bbcode_parser:
        loader = BBCodeParserLoader()
        loader.load_parser()
    return _bbcode_parser


class BBCodeParserLoader(object):
    def __init__(self, *args, **kwargs):
        parser = kwargs.pop('parser', None)
        if parser:
            self.parser = parser
        else:
            global _bbcode_parser
            _bbcode_parser = BBCodeParser()
            self.parser = _bbcode_parser

    def load_parser(self):
        # Init default BBCode placeholders
        self.init_default_bbcode_placeholders()

        # Init placeholders registered in 'bbcode_placeholders' modules
        self.init_bbcode_placeholders()

        # Init default BBCode tags
        self.init_default_bbcode_tags()

        # Init renderers registered in 'bbcode_tags' modules
        self.init_bbcode_tags()

        # Init custom renderers defined in BBCodeTag model instances
        if bbcode_settings.BBCODE_ALLOW_CUSTOM_TAGS:
            self.init_custom_bbcode_tags()

        # Init smilies
        if bbcode_settings.BBCODE_ALLOW_SMILIES:
            self.init_bbcode_smilies()

    def init_default_bbcode_placeholders(self):
        """
        Find the default placeholders and makes them available for the parser.
        """
        import precise_bbcode.bbcode.defaults.placeholder
        for placeholder_klass in get_subclasses(
                precise_bbcode.bbcode.defaults.placeholder, BBCodePlaceholder):
            setattr(placeholder_klass, 'default_placeholder', True)
            self.parser.add_placeholder(placeholder_klass)

    def init_bbcode_placeholders(self):
        """
        Call the BBCode placeholder pool to fetch all the module-based placeholders
        and initializes them.
        """
        from precise_bbcode.placeholder_pool import placeholder_pool
        placeholders = placeholder_pool.get_placeholders()
        for placeholder in placeholders:
            self.parser.add_placeholder(placeholder)

    def init_default_bbcode_tags(self):
        """
        Find the default bbcode tags and makes them available for the parser.
        """
        import precise_bbcode.bbcode.defaults.tag
        for tag_klass in get_subclasses(
                precise_bbcode.bbcode.defaults.tag, BBCodeTag):
            setattr(tag_klass, 'default_tag', True)
            self.parser.add_bbcode_tag(tag_klass)

    def init_bbcode_tags(self):
        """
        Call the BBCode tag pool to fetch all the module-based tags and initializes
        their associated renderers.
        """
        from precise_bbcode.tag_pool import tag_pool
        tags = tag_pool.get_tags()
        for tag_def in tags:
            self.parser.add_bbcode_tag(tag_def)

    def init_custom_bbcode_tags(self):
        """
        Find the user-defined BBCode tags and initializes their associated renderers.
        """
        BBCodeTag = get_model('precise_bbcode', 'BBCodeTag')
        if BBCodeTag:
            custom_tags = BBCodeTag.objects.all()
            for tag in custom_tags:
                self.parser.add_bbcode_tag(tag.parser_tag_klass)

    def init_bbcode_smilies(self):
        """
        Find the user-defined smilies tags and register them to the BBCode parser.
        """
        SmileyTag = get_model('precise_bbcode', 'SmileyTag')
        if SmileyTag:
            custom_smilies = SmileyTag.objects.all()
            for smiley in custom_smilies:
                self.parser.add_smiley(smiley.code, smiley.html_code)
