# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from jinja2 import Markup
from jinja2.ext import Extension

from .shortcuts import render_bbcodes


def do_bbcode(text):
    return Markup(render_bbcodes(text))


class PreciseBBCodeExtension(Extension):
    def __init__(self, environment):
        super(PreciseBBCodeExtension, self).__init__(environment)

        self.environment.globals.update({
            'bbcode': do_bbcode,
        })
        self.environment.filters.update({
            'bbcode': do_bbcode,
        })


bbcode = PreciseBBCodeExtension
