# -*- coding: utf-8 -*-

# Standard library imports

# Third party imports
from precise_bbcode.tag_base import TagBase
from precise_bbcode.tag_pool import tag_pool

# Local application / specific library imports


class SubTag(TagBase):
    tag_name = "sub"

    def render(self, name, value, option=None, parent=None):
        return '<sub>%s</sub>' % value


class PreTag(TagBase):
    tag_name = "pre"
    render_embedded = False

    def render(self, name, value, option=None, parent=None):
        return '<pre>%s</pre>' % value


tag_pool.register_tag(SubTag)
tag_pool.register_tag(PreTag)
