# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.conf import settings

# Local application / specific library imports


# The HTML tag to make a line break
BBCODE_NEWLINE = getattr(settings, 'BBCODE_NEWLINE', '<br />')

# The HTML special characters to be escaped during the rendering process
escape_html = (
    ('&', '&amp;'),
    ('<', '&lt;'),
    ('>', '&gt;'),
    ('"', '&quot;'),
    ('\'', '&#39;'),
)
BBCODE_ESCAPE_HTML = getattr(settings, 'BBCODE_ESCAPE_HTML', escape_html)


# Should custom tags be allowed ?
BBCODE_ALLOW_CUSTOM_TAGS = getattr(settings, 'BBCODE_ALLOW_CUSTOM_TAGS', True)


# Other options
BBCODE_NORMALIZE_NEWLINES = getattr(settings, 'BBCODE_NORMALIZE_NEWLINES', True)
