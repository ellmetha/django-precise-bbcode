import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from precise_bbcode.conf import settings as bbcode_settings
from precise_bbcode.bbcode.placeholder import BBCodePlaceholder

__all__ = [
    'UrlBBCodePlaceholder',
    'EmailBBCodePlaceholder',
    'TextBBCodePlaceholder',
    'SimpleTextBBCodePlaceholder',
    'ColorBBCodePlaceholder',
    'NumberBBCodePlaceholder',
    'RangeBBCodePlaceholder',
    'ChoiceBBCodePlaceholder',
]


# Placeholder regexes
_email_re = re.compile(r'(\w+[.|\w])*@\[?(\w+[.])*\w+\]?', flags=re.I)
_text_re = re.compile(r'^\s*([\w]+)|([\w]+\S*)\s*', flags=(re.U | re.M))
_simpletext_re = re.compile(r'^[a-zA-Z0-9-+.,_ ]+$')
_color_re = re.compile(r'^([a-z]+|#[0-9abcdefABCDEF]{3,6})$')
_number_re = re.compile(r'^[+-]?\d+(?:(\.|,)\d+)?$')


class UrlBBCodePlaceholder(BBCodePlaceholder):
    name = 'url'

    def validate(self, content, extra_context=None):
        for xss in bbcode_settings.URL_XSS_FILTER:
            if xss in content:
                return False
        if content[:2] == '//':
            return False
        if '://' in content:
            v = URLValidator()
            try:
                v(content)
            except ValidationError:
                return False
        return True


class EmailBBCodePlaceholder(BBCodePlaceholder):
    name = 'email'
    pattern = _email_re


class TextBBCodePlaceholder(BBCodePlaceholder):
    name = 'text'
    pattern = _text_re


class SimpleTextBBCodePlaceholder(BBCodePlaceholder):
    name = 'simpletext'
    pattern = _simpletext_re


class ColorBBCodePlaceholder(BBCodePlaceholder):
    name = 'color'
    pattern = _color_re


class NumberBBCodePlaceholder(BBCodePlaceholder):
    name = 'number'
    pattern = _number_re


class RangeBBCodePlaceholder(BBCodePlaceholder):
    name = 'range'

    def validate(self, content, extra_context):
        try:
            value = float(content)
        except ValueError:
            return False

        try:
            min_content, max_content = extra_context.split(',')
            min_value, max_value = float(min_content), float(max_content)
        except ValueError:
            return False

        if not (value >= min_value and value <= max_value):
            return False

        return True


class ChoiceBBCodePlaceholder(BBCodePlaceholder):
    name = 'choice'

    def validate(self, content, extra_context):
        choices = extra_context.split(',')
        return content in choices
