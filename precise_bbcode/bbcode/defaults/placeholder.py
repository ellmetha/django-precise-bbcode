# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import re

# Third party imports
# Local application / specific library imports
from precise_bbcode.bbcode.placeholder import BBCodePlaceholder

__all__ = [
    'UrlBBCodePlaceholder',
    'EmailBBCodePlaceholder',
    'TextBBCodePlaceholder',
    'SimpleTextBBCodePlaceholder',
    'ColorBBCodePlaceholder',
    'NumberBBCodePlaceholder',
]


# Placeholder regex
_url_re = re.compile(r'(?im)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\([^\s()<>]+\))+(?:\([^\s()<>]+\)|[^\s`!()\[\]{};:\'".,<>?]))')
_email_re = re.compile(r'(\w+[.|\w])*@\[?(\w+[.])*\w+\]?', re.IGNORECASE)
_text_re = re.compile(r'^\s*([\w]+)|([\w]+\S*)\s*$', flags=re.UNICODE)
_simpletext_re = re.compile(r'^[a-zA-Z0-9-+.,_ ]+$')
_color_re = re.compile(r'^([a-z]+|#[0-9abcdefABCDEF]{3,6})$')
_number_re = re.compile(r'^[+-]?\d+(?:(\.|,)\d+)?$')


class UrlBBCodePlaceholder(BBCodePlaceholder):
    name = 'url'
    pattern = _url_re


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
