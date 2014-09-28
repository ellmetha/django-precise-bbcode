# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
# Local application / specific library imports
from precise_bbcode.bbcode import get_parser


default_app_config = 'precise_bbcode.apps.PreciseBbCodeAppConfig'


def render_bbcodes(text):
    """
    Given an input text, calls the BBCode parser to get the corresponding HTML output.
    """
    parser = get_parser()
    return parser.render(text)
