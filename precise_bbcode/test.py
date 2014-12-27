# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals

# Third party imports
# Local application / specific library imports
from .bbcode.tag import BBCodeTag
from .core.compat import force_str


def gen_bbcode_tag_klass(klass_attrs, options_attrs={}):
    # Construc the inner Options class
    options_klass = type(force_str('Options'), (), options_attrs)
    # Construct the outer BBCodeTag class
    tag_klass_attrs = klass_attrs
    tag_klass_attrs['Options'] = options_klass
    tag_klass = type(force_str('{}Tag'.format(tag_klass_attrs['name'])), (BBCodeTag, ), tag_klass_attrs)
    return tag_klass
