##############
Custom smilies
##############

*Django-precise-bbcode* does not come with some built-in smilies but supports adding custom smilies and emoticons through the Django admin.

To add a smiley, just go to the admin page and you will see a new 'Smileys' section. In this section you can create and edit custom smilies. The smileys defined through the Django admin are then used by the built-in BBCode parser to transform any *smiley code* to the corresponding HTML.

Adding a smiley consists in filling at least the following fields:

* ``code``: The smiley code - it's the textual shortcut that the end users will use to include emoticons inside their bbcode contents. This text can be composed of any character without whitespace characters (eg. ``;)`` or ``-_-``)
* ``image``: The smiley image

The size at which the emoticon image is rendered can also be specified by using the ``image_width`` and ``image_height`` fields.