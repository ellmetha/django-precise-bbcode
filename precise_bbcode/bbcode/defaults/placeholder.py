# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import re

# Third party imports
# Local application / specific library imports
from precise_bbcode.bbcode.placeholder import BaseBBCodePlaceholder

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
_domain_re = re.compile(r'^(?=.{4,255}$)([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9]\.)+[a-zA-Z0-9]{2,5}$')
_email_re = re.compile(r'(\w+[.|\w])*@\[?(\w+[.])*\w+\]?', re.IGNORECASE)
_text_re = re.compile(r'^\s*([\w]+)|([\w]+\S*)\s*$', flags=re.UNICODE)
_simpletext_re = re.compile(r'^[a-zA-Z0-9-+.,_ ]+$')
_color_re = re.compile(r'^([a-z]+|#[0-9abcdefABCDEF]{3,6})$')
_number_re = re.compile(r'^[+-]?\d+(?:(\.|,)\d+)?$')


class UrlBBCodePlaceholder(BaseBBCodePlaceholder):
    name = 'url'
    pattern = _url_re


class EmailBBCodePlaceholder(BaseBBCodePlaceholder):
    name = 'email'
    pattern = _email_re


class TextBBCodePlaceholder(BaseBBCodePlaceholder):
    name = 'text'
    pattern = _text_re


class SimpleTextBBCodePlaceholder(BaseBBCodePlaceholder):
    name = 'simpletext'
    pattern = _simpletext_re


class ColorBBCodePlaceholder(BaseBBCodePlaceholder):
    name = 'color'
    pattern = _color_re


class NumberBBCodePlaceholder(BaseBBCodePlaceholder):
    name = 'number'
    pattern = _number_re
