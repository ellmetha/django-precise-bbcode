Precise BBcodes settings
========================

This is a comprehensive list of all the settings *Django-precise-bbcode* provides. All settings are optional.

Parser settings
***************

``BBCODE_NEWLINE``
------------------

Default: ``'<br />'``

The HTML replacement code for a default newline.

``BBCODE_ESCAPE_HTML``
----------------------

Default::

    (
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ('"', '&quot;'),
        ('\'', '&#39;'),
    )

The list of all characters that must be escaped before rendering.

``BBCODE_ALLOW_CUSTOM_TAGS``
----------------------------

Default: ``True``

The flag indicating whether the custom BBCode tags (those defined by the end users through the Django admin) are allowed.

``BBCODE_NORMALIZE_NEWLINES``
-----------------------------

Default: ``True``

The flag indicating whether the newlines are normalized (if this is the case all newlines are replaced with ``\r\n``).

Smilies settings
****************

``BBCODE_ALLOW_SMILIES``
------------------------

Default: ``True``

The flag indicating whether the smilies (defined by the end users through the Django admin) are allowed.

``SMILIES_UPLOAD_TO``
---------------------

Default: ``'precise_bbcode/smilies'``

The media subdirectory where the smilies should be uploaded.
