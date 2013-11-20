# -*- coding: utf-8 -*-

# Standard library imports
import re

# Third party imports
from django.core.exceptions import ImproperlyConfigured

# Local application / specific library imports
from precise_bbcode.parser import BBCodeTagOptions
from precise_bbcode.utils.compat import with_metaclass


class TagBaseMetaclass(type):
    """
    Ensure the Tag subclasses have the required values and proceed to some
    validations.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(TagBaseMetaclass, cls).__new__
        parents = [base for base in bases if isinstance(base, TagBaseMetaclass)]
        if not parents:
            # Stop here if we are considering TagBase and not one of its subclasses
            return super_new(cls, name, bases, attrs)
        new_tag = super_new(cls, name, bases, attrs)

        # Validates the tag name
        if not hasattr(new_tag, 'tag_name'):
            raise ImproperlyConfigured(
                'TagBase subclasses must have a tag_name attribute'
            )
        if not new_tag.tag_name:
            raise ImproperlyConfigured(
                'The tag_name attribute associated with TagBase subclasses cannot be None'
            )
        if not re.match('^[A-Za-z0-9]+$', new_tag.tag_name):
            raise ValueError(
                """The tag_name attribute associated with {!r} is not valid: a tag name must be strictly
                composed of letters and numbers""".format(name)
            )

        return new_tag


class TagBase(with_metaclass(TagBaseMetaclass, BBCodeTagOptions)):
    tag_name = None

    def render(self, name, value, option=None, parent=None):
        """
        The render function is used to transform a BBCodeTag and its context (value, option) to
        the corresponding HTML output.

            tag_name
                The name of the tag being rendered.
            value
                The context between start and end tags, or None for standalone tags.
                Whether this has been rendered depends on render_embedded tag option.
            option
                The value of an option passed to the tag.
            parent
                The parent BBCodeTagOptions, if the tag is being rendered inside another tag,
                otherwise None.
        """
        # The default implementation will raise a NotImplementedError to ensure
        # that any subclasses must override this method
        raise NotImplementedError

    @classmethod
    def _options(cls):
        options = {}
        tag_option_attrs = vars(BBCodeTagOptions)
        for key, value in vars(cls).items():
            if key in tag_option_attrs and not key.startswith('__'):
                options[key] = value
        return options
