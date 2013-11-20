# -*- coding: utf-8 -*-

# Standard library imports
import re

# Third party imports
from django import template
from django.template import Node
from django.template import TemplateSyntaxError
from django.template import TokenParser
from django.template import Variable
from django.utils.safestring import mark_safe

# Local application / specific library imports
from precise_bbcode.utils.bbcode import render_bbcodes
from precise_bbcode.utils.compat import string_types


register = template.Library()


class BBCodeNode(Node):
    def __init__(self, filter_expression, asvar=None):
        self.filter_expression = filter_expression
        self.asvar = asvar
        if isinstance(self.filter_expression.var, string_types):
            self.filter_expression.var = Variable("'{!s}'".format(self.filter_expression.var))

    def render(self, context):
        output = self.filter_expression.resolve(context)
        value = mark_safe(render_bbcodes(output))
        if self.asvar:
            context[self.asvar] = value
            return ''
        else:
            return value


@register.filter(is_safe=True)
def bbcode(value):
    return render_bbcodes(value)


@register.tag('bbcode')
def do_bbcode_rendering(parser, token):
    """
    This will render a string containing bbcodes to the corresponding HTML markup.

    Usage::

        {%  bbcode "[b]hello world![/b]" %}

    You can use variables instead of constant strings to render bbcode stuff::

        {%  bbcode contentvar %}

    It is possible to store the rendered string into a variable::

        {%  bbcode "[b]hello world![/b]" as renderedvar %}
    """
    class BBCodeParser(TokenParser):
        def top(self):
            value = self.value()

            # Transform single-quoted strings to maintain backward compatibility
            if value[0] == "'":
                m = re.match("^'([^']+)'(\|.*$)", value)
                if m:
                    value = '"%s"%s' % (m.group(1).replace('"', '\\"'), m.group(2))
                elif value[-1] == "'":
                    value = '"%s"' % value[1:-1].replace('"', '\\"')

            asvar = None
            while self.more():
                tag = self.tag()
                if tag == 'as':
                    asvar = self.tag()
                else:
                    raise TemplateSyntaxError(
                        "Only option for 'bbcode' is 'as VAR'.")
            return value, asvar
    value, asvar = BBCodeParser(token.contents).top()
    return BBCodeNode(parser.compile_filter(value), asvar)
