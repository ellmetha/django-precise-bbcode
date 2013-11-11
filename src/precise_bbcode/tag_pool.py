# -*- coding: utf-8 -*-

# Standard library imports

# Third party imports
from django.core.exceptions import ImproperlyConfigured

# Local application / specific library imports
from precise_bbcode.tag_base import TagBase
from precise_bbcode.utils.django_load import load


class TagAlreadyRegistered(Exception):
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
        # A registered tag must be a subclass of TagBase
        if not issubclass(tag, TagBase):
            raise ImproperlyConfigured(
                'BBCode Tags must be subclasses of TagBase, {!r} is not'.format(tag)
            )
        # Two tag with the same names can't be registered
        tag_name = tag.__name__
        if tag_name in self.tags:
            raise TagAlreadyRegistered(
                'Cannot register {!r}, a tag with this name ({!r}) is already registered'.format(tag, tag_name)
            )

        self.tags[tag_name] = tag

    def unregister_tag(self, tag):
        """
        Unregister the given tag(s).
        If a tag appears to be not registered, a TagNotRegistered exception will be raised.
        """
        tag_name = tag.__name__
        if tag_name not in self.tags:
            raise TagNotRegistered(
                'The tag {!r} is not registered'.format(tag)
            )
        del self.tags[tag_name]

    def get_tags(self):
        self.discover_tags()
        return self.tags.values()


tag_pool = TagPool()
