# -*- coding: utf-8 -*-

# Standard library imports
import re

# Third party imports
from precise_bbcode.bbcode.placeholder import BBCodePlaceholder
from precise_bbcode.placeholder_pool import placeholder_pool

# Local application / specific library imports


class PhoneNumberBBCodePlaceholder(BBCodePlaceholder):
    name = 'phonenumber'
    pattern = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')


class StartsWithBBCodePlaceholder(BBCodePlaceholder):
    name = 'startswith'

    def validate(self, content, extra_context):
        return content.startswith(extra_context)


placeholder_pool.register_placeholder(PhoneNumberBBCodePlaceholder)
placeholder_pool.register_placeholder(StartsWithBBCodePlaceholder)
