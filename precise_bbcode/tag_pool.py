# -*- coding: utf-8 -*-

# Standard library imports

# Third party imports
from django.core.exceptions import ImproperlyConfigured

# Local application / specific library imports
from .bbcode.tag import BBCodeTag
from .conf import settings as bbcode_settings
from .core.loading import load
from .models import BBCodeTag as DbBBCodeTag


class TagAlreadyRegistered(Exception):
    pass


class TagAlreadyCreated(Exception):
    pass


class TagNotRegistered(Exception):
    pass


class TagPool(object):
    """
    BBCode tags are registered with the TagPool using the register() method. It makes them
    available to the BBCode parser.
    """

    def __init__(self):
        self.tags = {}
        self.discovered = False

    def discover_tags(self):
        if self.discovered:
            return
        self.discovered = True
        load('bbcode_tags')

    def register_tag(self, tag):
        """
        Registers the given tag(s).
        If a tag appears to be already registered, a TagAlreadyRegistered exception will be raised.
        """
        # A registered tag must be a subclass of BBCodeTag
        if not issubclass(tag, BBCodeTag):
            raise ImproperlyConfigured(
                'BBCode Tags must be subclasses of BBCodeTag, {!r} is not'.format(tag)
            )

        # Two tag with the same names can't be registered
        tag_name = tag.name
        if tag_name in self.tags:
            raise TagAlreadyRegistered(
                'Cannot register {!r}, a tag with this name ({!r}) is already registered'.format(tag, tag_name)
            )

        # The tag cannot be registered if it is already stored as bbcode tag in the database
        bbcode_tag_qs = DbBBCodeTag.objects.filter(tag_name=tag_name)
        if bbcode_tag_qs.exists() and bbcode_settings.BBCODE_ALLOW_CUSTOM_TAGS:
            raise TagAlreadyCreated(
                """Cannot register {!r}, a tag with this name ({!r}) is
                already stored in your database: {}""".format(tag, tag_name, bbcode_tag_qs[0])
            )

        self.tags[tag_name] = tag

    def unregister_tag(self, tag):
        """
        Unregister the given tag(s).
        If a tag appears to be not registered, a TagNotRegistered exception will be raised.
        """
        tag_name = tag.name
        if tag_name not in self.tags:
            raise TagNotRegistered(
                'The tag {!r} is not registered'.format(tag)
            )
        del self.tags[tag_name]

    def get_tags(self):
        self.discover_tags()
        return self.tags.values()


tag_pool = TagPool()
