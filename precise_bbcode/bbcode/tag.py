# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import inspect
import re

# Third party imports
from django.core.exceptions import ImproperlyConfigured

# Local application / specific library imports
from precise_bbcode.bbcode.exceptions import InvalidBBCodePlaholder
from precise_bbcode.bbcode.regexes import placeholder_content_re
from precise_bbcode.bbcode.regexes import placeholder_re
from precise_bbcode.conf import settings as bbcode_settings
from precise_bbcode.core.compat import with_metaclass
from precise_bbcode.core.utils import replace


class BBCodeTagBase(type):
    """
    Metaclass for all BBCode tags.
    This metaclass ensure that the BBCode tags subclasses have the required values
    and proceed to some validations.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(BBCodeTagBase, cls).__new__
        parents = [base for base in bases if isinstance(base, BBCodeTagBase)]

        if not parents:
            # Stop here if we are considering the top-level class to which the
            # current metaclass was applied and not one of its subclasses.
            # eg. BBCodeTag
            return super_new(cls, name, bases, attrs)

        # Pop the option metadata from the class attributes
        options_klass = attrs.pop('Options', None)

        # Construct the BBCode tag class
        new_tag = super_new(cls, name, bases, attrs)

        # Validates the tag name
        if not hasattr(new_tag, 'name'):
            raise ImproperlyConfigured(
                'BBCodeTag subclasses must have a \'name\' attribute'
            )
        if not new_tag.name:
            raise ImproperlyConfigured(
                'The \'name\' attribute associated with BBCodeTag subclasses cannot be None'
            )
        if not re.match('^[^\s=]+$', new_tag.name):
            raise ImproperlyConfigured(
                """The \'name\' attribute associated with {!r} is not valid: a tag name must be strictly
                composed of non-white-space characters""".format(name)
            )

        # Validates the BBCode definition: a BBCode class with a definition string cannot be
        # created without a format string. The reverse is also true.
        if (new_tag.definition_string and not new_tag.format_string) \
                or (not new_tag.definition_string and new_tag.format_string):
            raise ImproperlyConfigured(
                """{!r} is not valid: the \'definition_string\' attribute cannot be specified without defining
                the related \'format_string\'""".format(name)
            )
        # TODO: Some additional checks should be added here

        # Initializes the '_options' attribute
        if options_klass:
            option_attrs = inspect.getmembers(options_klass, lambda a: not(inspect.isroutine(a)))
            options_kwargs = dict([a for a in option_attrs if not(a[0].startswith('__') and a[0].endswith('__'))])
            setattr(new_tag, '_options', BBCodeTagOptions(**options_kwargs))
        else:
            setattr(new_tag, '_options', BBCodeTagOptions())

        return new_tag


class BBCodeTag(with_metaclass(BBCodeTagBase)):
    name = None
    definition_string = None
    format_string = None

    def do_render(self, parser, value, option=None, parent=None):
        """
        This method is called by the BBCode parser to render the content of
        each BBCode tag.
        The default implementation will use a generic rendering method if the
        BBCode tag is defined by a definition string and a format string. In
        any other case, the 'render' method will be called. The latest should
        be overidden in any subclasses that is not based on a defintion string
        and a format string.
        """
        if self.definition_string and self.format_string:
            return self._render_default(parser, value, option, parent)
        return self.render(value, option, parent)

    def render(self, value, option=None, parent=None):
        """
        The render function is used to transform a BBCodeTag and its context (value, option) to
        the corresponding HTML output.

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
        # that any subclasses must override this method if the definition string
        # and the format string are not used.
        raise NotImplementedError

    def _render_default(self, parser, value, option=None, parent=None):
        placeholders = re.findall(placeholder_re, self.definition_string)
        # Get the format data
        fmt = {}
        if len(placeholders) == 1:
            fmt.update({placeholders[0]: value})
        elif len(placeholders) == 2:
            fmt.update({placeholders[1]: value, placeholders[0]: replace(option, bbcode_settings.BBCODE_ESCAPE_HTML) if option else ''})

        # Semantic validation
        valid = self._validate_format(parser, fmt)
        if not valid and option:
            return self.definition_string.format(**fmt)
        elif not valid:
            return self.definition_string.replace('=', '').format(**fmt)

        # Before rendering, it's necessary to escape the included braces: '{' and '}' ; some of them could not be placeholders
        escaped_format_string = self.format_string.replace('{', '{{').replace('}', '}}')
        for placeholder in fmt.keys():
            escaped_format_string = escaped_format_string.replace('{' + placeholder + '}', placeholder)

        # Return the rendered data
        return escaped_format_string.format(**fmt)

    def _validate_format(self, parser, format_dict):
        """
        Validates the given format dictionary. Each key of this dict refers to a specific BBCode placeholder type.
        eg. {TEXT} or {TEXT1} refer to the 'TEXT' BBCode placeholder type.
        Each content is validated according to its associated placeholder type.
        """
        for placeholder_string, content in format_dict.items():
            try:
                placeholder_results = re.findall(placeholder_content_re, placeholder_string)
                assert len(placeholder_results)
                placeholder_type, _, extra_context = placeholder_results[0]
                valid_content = parser.placeholders[placeholder_type.upper()].validate(content, extra_context=extra_context[1:])
                assert valid_content and valid_content is not None
            except KeyError:
                raise InvalidBBCodePlaholder(placeholder_type)
            except AssertionError:
                return False
        return True


class BBCodeTagOptions(object):
    # Force the closing of this tag after a newline
    newline_closes = False
    # Force the closing of this tag after the start of the same tag
    same_tag_closes = False
    # Force the closing of this tag after the end of another tag
    end_tag_closes = False
    # This tag does not have a closing tag
    standalone = False
    # The embedded tags will be rendered
    render_embedded = True
    # The embedded newlines will be converted to markup
    transform_newlines = True
    # The HTML characters inside this tag will be escaped
    escape_html = True
    # Replace URLs with link markups inside this tag
    replace_links = True
    # Strip leading and trailing whitespace inside this tag
    strip = False
    # Swallow the first trailing newline
    swallow_trailing_newline = False

    # The following options will be usefull for BBCode editors
    helpline = None
    display_on_editor = True

    def __init__(self, **kwargs):
        for attr, value in list(kwargs.items()):
            setattr(self, attr, bool(value))
