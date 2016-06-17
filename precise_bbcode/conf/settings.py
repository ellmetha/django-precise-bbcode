# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings


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


# Should the built-in tags be disabled?
BBCODE_DISABLE_BUILTIN_TAGS = getattr(settings, 'BBCODE_DISABLE_BUILTIN_TAGS', False)


# Should custom tags be allowed?
BBCODE_ALLOW_CUSTOM_TAGS = getattr(settings, 'BBCODE_ALLOW_CUSTOM_TAGS', True)


# Other options
BBCODE_NORMALIZE_NEWLINES = getattr(settings, 'BBCODE_NORMALIZE_NEWLINES', True)


# Smileys options
BBCODE_ALLOW_SMILIES = getattr(settings, 'BBCODE_ALLOW_SMILIES', True)
SMILIES_UPLOAD_TO = getattr(settings, 'BBCODE_SMILIES_UPLOAD_TO', 'precise_bbcode/smilies')
