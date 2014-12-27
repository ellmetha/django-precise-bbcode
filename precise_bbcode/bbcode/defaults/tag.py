# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import re

# Third party imports
# Local application / specific library imports
from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.conf import settings as bbcode_settings
from precise_bbcode.core.utils import replace


class StrongBBCodeTag(BBCodeTag):
    name = 'b'
    definition_string = '[b]{TEXT}[/b]'
    format_string = '<strong>{TEXT}</strong>'


class ItalicBBCodeTag(BBCodeTag):
    name = 'i'
    definition_string = '[i]{TEXT}[/i]'
    format_string = '<em>{TEXT}</em>'


class UnderlineBBCodeTag(BBCodeTag):
    name = 'u'
    definition_string = '[u]{TEXT}[/u]'
    format_string = '<u>{TEXT}</u>'


class StrikeBBCodeTag(BBCodeTag):
    name = 's'
    definition_string = '[s]{TEXT}[/s]'
    format_string = '<strike>{TEXT}</strike>'


class ListBBCodeTag(BBCodeTag):
    name = 'list'

    class Options:
        transform_newlines = True
        strip = True

    def render(self, value, option=None, parent=None):
        css_opts = {
            '1': 'decimal', '01': 'decimal-leading-zero',
            'a': 'lower-alpha', 'A': 'upper-alpha',
            'i': 'lower-roman', 'I': 'upper-roman',
        }
        list_tag = 'ol' if option in css_opts else 'ul'
        list_tag_css = ' style="list-style-type:{};"'.format(css_opts[option]) if list_tag == 'ol' else ''
        rendered = '<{tag}{css}>{content}</{tag}>'.format(tag=list_tag, css=list_tag_css, content=value)
        return rendered


class ListItemBBCodeTag(BBCodeTag):
    name = '*'
    definition_string = '[*]{TEXT}'
    format_string = '<li>{TEXT}</li>'

    class Options:
        newline_closes = True
        same_tag_closes = True
        end_tag_closes = True
        strip = True


class QuoteBBCodeTag(BBCodeTag):
    name = 'quote'
    definition_string = '[quote]{TEXT}[/quote]'
    format_string = '<blockquote>{TEXT}</blockquote>'

    class Options:
        strip = True


class CodeBBCodeTag(BBCodeTag):
    name = 'code'
    definition_string = '[code]{TEXT}[/code]'
    format_string = '<code>{TEXT}</code>'

    class Options:
        render_embedded = False


class CenterBBCodeTag(BBCodeTag):
    name = 'center'
    definition_string = '[center]{TEXT}[/center]'
    format_string = '<div style="text-align:center;">{TEXT}</div>'


class ColorBBCodeTag(BBCodeTag):
    name = 'color'
    definition_string = '[color={COLOR}]{TEXT}[/color]'
    format_string = '<span style="color:{COLOR};">{TEXT}</span>'


class UrlBBCodeTag(BBCodeTag):
    name = 'url'

    _domain_re = re.compile(r'^(?=.{4,255}$)([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9]\.)+[a-zA-Z0-9]{2,5}$')

    class Options:
        replace_links = False

    def render(self, value, option=None, parent=None):
        href = replace(option, bbcode_settings.BBCODE_ESCAPE_HTML) if option else value
        if '://' not in href and self._domain_re.match(href):
            href = 'http://' + href
        content = value if option else href
        # Render
        return '<a href="{}">{}</a>'.format(href, content or href)


class ImgBBCodeTag(BBCodeTag):
    name = 'img'
    definition_string = '[img]{URL}[/img]'
    format_string = '<img src="{URL}" alt="" />'

    class Options:
        replace_links = False
