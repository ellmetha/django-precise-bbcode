# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured

from .bbcode.placeholder import BBCodePlaceholder
from .core.loading import load


class PlaceholderAlreadyRegistered(Exception):
    pass


class PlaceholderNotRegistered(Exception):
    pass


class PlaceholderPool(object):
    """
    BBCode placeholders are registered with the PlaceholderPool using the register() method. It
    makes them available to the BBCode parser.
    """

    def __init__(self):
        self.placeholders = {}
        self.discovered = False

    def discover_placeholders(self):
        if self.discovered:
            return
        self.discovered = True
        load('bbcode_placeholders')

    def register_placeholder(self, placeholder):
        """
        Registers the given placeholder(s).
        If a placeholder appears to be already registered, a PlaceholderAlreadyRegistered exception
        will be raised.
        """
        # A registered placeholder must be a subclass of BBCodePlaceholder
        if not issubclass(placeholder, BBCodePlaceholder):
            raise ImproperlyConfigured(
                'BBCode Placeholders must be subclasses of BBCodePlaceholder, '
                '{!r} is not'.format(placeholder)
            )

        # Two placeholders with the same names can't be registered
        placeholder_name = placeholder.name
        if placeholder_name in self.placeholders:
            raise PlaceholderAlreadyRegistered(
                'Cannot register {!r}, a placeholder with this name ({!r}) '
                'is already registered'.format(
                    placeholder, placeholder_name)
            )

        self.placeholders[placeholder_name] = placeholder

    def unregister_placeholder(self, placeholder):
        """
        Unregister the given placeholder(s).
        If a placeholder appears to be not registered, a PlaceholderNotRegistered exception will be
        raised.
        """
        placeholder_name = placeholder.name
        if placeholder_name not in self.placeholders:
            raise PlaceholderNotRegistered(
                'The placeholder {!r} is not registered'.format(placeholder)
            )
        del self.placeholders[placeholder_name]

    def get_placeholders(self):
        self.discover_placeholders()
        return self.placeholders.values()


placeholder_pool = PlaceholderPool()
