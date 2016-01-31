# -*- coding: utf-8 -*-

import sys

from django import template
from django.template import Node
from django.template import TemplateSyntaxError
from django.template import Variable
from django.template.defaultfilters import stringfilter
from django.utils import six
from django.utils.safestring import mark_safe

from precise_bbcode.shortcuts import render_bbcodes


register = template.Library()


class BBCodeNode(Node):
    def __init__(self, filter_expression, asvar=None):
        self.filter_expression = filter_expression
        self.asvar = asvar
        if isinstance(self.filter_expression.var, six.string_types):
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
@stringfilter
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
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError('\'{0}\' takes at least one argument'.format(bits[0]))
    value = parser.compile_filter(bits[1])

    remaining = bits[2:]
    asvar = None
    seen = set()

    while remaining:
        option = remaining.pop(0)
        if option in seen:
            raise TemplateSyntaxError(
                'The \'{0}\' option was specified more than once.'.format(option))
        elif option == 'as':
            try:
                var_value = remaining.pop(0)
            except IndexError:
                msg = 'No argument provided to the \'{0}\' tag for the as option.'.format(bits[0])
                six.reraise(TemplateSyntaxError, TemplateSyntaxError(msg), sys.exc_info()[2])
            asvar = var_value
        else:
            raise TemplateSyntaxError(
                'Unknown argument for \'{0}\' tag: \'{1}\'. The only options '
                'available is \'as VAR\'.'.format(bits[0], option))
        seen.add(option)

    return BBCodeNode(value, asvar)
