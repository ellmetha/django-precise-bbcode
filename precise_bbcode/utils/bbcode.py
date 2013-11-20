# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
# Local application / specific library imports
from precise_bbcode.parser import get_parser


def render_bbcodes(text):
    """
    Given an input text, calls the BBCode parser to get the corresponding HTML output.
    """
    parser = get_parser()
    return parser.render(text)
