# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import re

# Third party imports
# Local application / specific library imports


# BBCode regex
bbcodde_standard_re = r"^\[(?P<start_name>[A-Za-z0-9]*)(=\{[A-Za-z0-9]*\})?\]\{[A-Za-z0-9]*\}\[/(?P<end_name>[A-Za-z0-9]*)\]$"
bbcodde_standalone_re = r"^\[(?P<start_name>[A-Za-z0-9]*)(=\{[A-Za-z0-9]*\})?\]\{?[A-Za-z0-9]*\}?$"
bbcode_content_re = re.compile(r'^\[[A-Za-z0-9]*\](?P<content>.*)\[/[A-Za-z0-9]*\]')


class BBCodeTagOptions(object):
    # Force the closing of this tag after a newline
    newline_closes = False
    # Force the closing of this tag after the start of the same tag
    same_tag_closes = False
    # Force the closing of this tag after the end of another tag
    end_tag_closes = False
    # This tag does not have a closing tag
    standalone = False
    # The embedded tags will be rendered
    render_embedded = True
    # The embedded newlines will be converted to markup
    transform_newlines = True
    # The HTML characters inside this tag will be escaped
    escape_html = True
    # Replace URLs with link markups inside this tag
    replace_links = True
    # Strip leading and trailing whitespace inside this tag
    strip = False
    # Swallow the first trailing newline
    swallow_trailing_newline = False

    # The following options will be usefull for BBCode editors
    helpline = None
    display_on_editor = True

    def __init__(self, **kwargs):
        for attr, value in list(kwargs.items()):
            setattr(self, attr, bool(value))
