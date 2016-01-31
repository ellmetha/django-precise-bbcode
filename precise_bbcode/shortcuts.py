# -*- coding: utf-8 -*-

from precise_bbcode.bbcode import get_parser


def render_bbcodes(text):
    """
    Given an input text, calls the BBCode parser to get the corresponding HTML output.
    """
    parser = get_parser()
    return parser.render(text)
