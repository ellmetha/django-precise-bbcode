# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django import template

# Local application / specific library imports
from precise_bbcode.utils.bbcode import render_bbcodes


register = template.Library()


@register.filter(is_safe=True)
def bbcode(value):
    return render_bbcodes(value)
