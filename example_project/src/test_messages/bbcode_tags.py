# -*- coding: utf-8 -*-

# Standard library imports

# Third party imports
from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.tag_pool import tag_pool

# Local application / specific library imports


class SubTag(BBCodeTag):
    name = 'sub'

    def render(self, name, value, option=None, parent=None):
        return '<sub>%s</sub>' % value


class PreTag(BBCodeTag):
    name = 'pre'
    render_embedded = False

    def render(self, name, value, option=None, parent=None):
        return '<pre>%s</pre>' % value


class SizeTag(BBCodeTag):
    name = 'size'
    definition_string = '[size={RANGE=4,7}]{TEXT}[/size]'
    format_string = '<span class="font-size:{RANGE=4,7};">{TEXT}</span>'


tag_pool.register_tag(SubTag)
tag_pool.register_tag(PreTag)
tag_pool.register_tag(SizeTag)
