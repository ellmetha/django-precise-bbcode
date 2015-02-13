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


pkg_resources = __import__('pkg_resources')
distribution = pkg_resources.get_distribution('django-precise-bbcode')
__version__ = distribution.version
