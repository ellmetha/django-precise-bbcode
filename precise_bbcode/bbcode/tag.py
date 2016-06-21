# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import inspect
import re

from precise_bbcode.bbcode.exceptions import InvalidBBCodePlaholder
from precise_bbcode.bbcode.exceptions import InvalidBBCodeTag
from precise_bbcode.bbcode.regexes import bbcodde_standalone_re
from precise_bbcode.bbcode.regexes import bbcodde_standard_re
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

        # Pop the option metadata from the class attributes
        options_klass = attrs.pop('Options', None)

        # Construct the BBCode tag class
        new_tag = super_new(cls, name, bases, attrs)

        # Validates the tag name
        if not hasattr(new_tag, 'name'):
            raise InvalidBBCodeTag(
                'BBCodeTag subclasses must have a \'name\' attribute'
            )
        if not new_tag.name:
            raise InvalidBBCodeTag(
                'The \'name\' attribute associated with BBCodeTag subclasses cannot be None'
            )
        if not re.match('^[^\s=]+$', new_tag.name):
            raise InvalidBBCodeTag(
                """The \'name\' attribute associated with {!r} is not valid: a tag name must be
                strictly composed of non-white-space characters and the '=' character is not
                allowed""".format(name)
            )

        # Initializes the '_options' attribute
        if options_klass:
            option_attrs = inspect.getmembers(options_klass, lambda a: not(inspect.isroutine(a)))
            options_kwargs = dict(
                [a for a in option_attrs if not(a[0].startswith('__') and a[0].endswith('__'))])
            setattr(new_tag, '_options', BBCodeTagOptions(**options_kwargs))
        else:
            setattr(new_tag, '_options', BBCodeTagOptions())

        # Validates the BBCode definition: a BBCode class with a definition string cannot be
        # created without a format string. The reverse is also true.
        if (new_tag.definition_string and not new_tag.format_string) \
                or (not new_tag.definition_string and new_tag.format_string):
            raise InvalidBBCodeTag(
                """{!r} is not valid: the \'definition_string\' attribute cannot be specified without defining
                the related \'format_string\'""".format(name)
            )

        if new_tag.definition_string and new_tag.format_string:
            # Check whether the tag is correctly defined according to a bbcode tag regex
            tag_re = bbcodde_standard_re if not new_tag._options.standalone \
                else bbcodde_standalone_re
            valid_bbcode_tag = re.search(tag_re, new_tag.definition_string)
            if not valid_bbcode_tag:
                raise InvalidBBCodeTag('The BBCode definition you provided is not valid')

            re_groups = re.search(tag_re, new_tag.definition_string).groupdict()

            # The beginning and end tag names must be the same
            if not (new_tag._options.standalone or new_tag._options.newline_closes or
                    new_tag._options.same_tag_closes or new_tag._options.end_tag_closes) \
                    and re_groups['start_name'] != re_groups['end_name']:
                raise InvalidBBCodeTag(
                    'This BBCode tag dit not validate because the start tag and the tag names are '
                    'not the same')

            # The used placeholders must be the same in the tag definition and in the HTML
            # replacement code
            def_placeholders = re.findall(placeholder_re, new_tag.definition_string)
            html_placeholders = re.findall(placeholder_re, new_tag.format_string)
            if set(def_placeholders) != set(html_placeholders):
                raise InvalidBBCodeTag(
                    'The placeholders defined in the tag definition must be present in the HTML '
                    'replacement code!')

            # ... and two placeholders must not have the same name
            def_placeholders_uniques = list(set(def_placeholders))
            if sorted(def_placeholders) != sorted(def_placeholders_uniques):
                raise InvalidBBCodeTag(
                    'The placeholders defined in the tag definition must be strictly uniques')

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
        be overidden in any subclasses that is not based on a definition string
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
                The parent BBCodeTag instance, if the tag is being rendered inside another tag,
                otherwise None.
        """
        # The default implementation will raise a NotImplementedError to ensure
        # that any subclasses must override this method if the definition string
        # and the format string are not used.
        raise NotImplementedError

    def _render_default(self, parser, value, option=None, parent=None):
        placeholders = re.findall(placeholder_re, self.definition_string)
        # Get the format data
        fmt = {}
        if len(placeholders) == 1:
            fmt.update({placeholders[0]: value})
        elif len(placeholders) == 2:
            fmt.update({
                placeholders[1]: value,
                placeholders[0]: replace(option, bbcode_settings.BBCODE_ESCAPE_HTML) if option else ''  # noqa
            })

        # Semantic validation
        valid = self._validate_format(parser, fmt)
        if not valid and option:
            return self.definition_string.format(**fmt)
        elif not valid:
            return self.definition_string.format(**fmt).replace('=', '')

        # Before rendering, it's necessary to escape the included braces: '{' and '}' ; some of them
        # could not be placeholders
        escaped_format_string = self.format_string.replace('{', '{{').replace('}', '}}')
        for placeholder in fmt.keys():
            escaped_format_string = escaped_format_string.replace(
                '{' + placeholder + '}', placeholder)

        # Return the rendered data
        return escaped_format_string.format(**fmt)

    def _validate_format(self, parser, format_dict):
        """
        Validates the given format dictionary. Each key of this dict refers to a specific BBCode
        placeholder type.
        eg. {TEXT} or {TEXT1} refer to the 'TEXT' BBCode placeholder type.
        Each content is validated according to its associated placeholder type.
        """
        for placeholder_string, content in format_dict.items():
            try:
                placeholder_results = re.findall(placeholder_content_re, placeholder_string)
                assert len(placeholder_results)
                placeholder_type, _, extra_context = placeholder_results[0]
                valid_content = parser.placeholders[placeholder_type.upper()].validate(
                    content, extra_context=extra_context[1:])
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
    # This tag does not have a closing tag
    standalone = False
    # The embedded tags will be rendered
    render_embedded = True
    # The embedded newlines will be converted to markup
    transform_newlines = True
    # The HTML characters inside this tag will be escaped
    escape_html = True
    # Replace URLs with link markups inside this tag
    replace_links = True
    # Strip leading and trailing whitespace inside this tag
    strip = False
    # Swallow the first trailing newline
    swallow_trailing_newline = False

    # The following options will be usefull for BBCode editors
    helpline = None
    display_on_editor = True

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
