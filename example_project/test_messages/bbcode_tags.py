import re

from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.tag_pool import tag_pool


color_re = re.compile(r'^([a-z]+|#[0-9abcdefABCDEF]{3,6})$')


class SubTag(BBCodeTag):
    name = 'sub'

    def render(self, value, option=None, parent=None):
        return '<sub>%s</sub>' % value


class PreTag(BBCodeTag):
    name = 'pre'
    render_embedded = False

    def render(self, value, option=None, parent=None):
        return '<pre>%s</pre>' % value


class SizeTag(BBCodeTag):
    name = 'size'
    definition_string = '[size={RANGE=4,7}]{TEXT}[/size]'
    format_string = '<span style="font-size:{RANGE=4,7}px;">{TEXT}</span>'


class FruitTag(BBCodeTag):
    name = 'fruit'
    definition_string = '[fruit]{CHOICE=tomato,orange,apple}[/fruit]'
    format_string = '<h5>{CHOICE=tomato,orange,apple}</h5>'


class PhoneLinkTag(BBCodeTag):
    name = 'phone'
    definition_string = '[phone]{PHONENUMBER}[/phone]'
    format_string = '<a href="tel:{PHONENUMBER}">{PHONENUMBER}</a>'

    def render(self, value, option=None, parent=None):
        href = 'tel:{}'.format(value)
        return '<a href="{0}">{1}</a>'.format(href, value)


class StartsWithATag(BBCodeTag):
    name = 'startswitha'
    definition_string = '[startswitha]{STARTSWITH=a}[/startswitha]'
    format_string = '<span>{STARTSWITH=a}</span>'


class RoundedBBCodeTag(BBCodeTag):
    name = 'rounded'

    class Options:
        strip = False

    def render(self, value, option=None, parent=None):
        if option and re.search(color_re, option) is not None:
            return '<div class="rounded" style="border-color:{};">{}</div>'.format(option, value)
        return '<div class="rounded">{}</div>'.format(value)


tag_pool.register_tag(SubTag)
tag_pool.register_tag(PreTag)
tag_pool.register_tag(SizeTag)
tag_pool.register_tag(FruitTag)
tag_pool.register_tag(PhoneLinkTag)
tag_pool.register_tag(StartsWithATag)
tag_pool.register_tag(RoundedBBCodeTag)
