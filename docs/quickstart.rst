Quickstart
==========

Install the project using::

    pip install django-precise-bbcode

Add ``precise_bbcode`` to ``INSTALLED_APPS`` in your project's settings module:::

    INSTALLED_APPS += (
        # other apps
        'precise_bbcode',
    )

Then install the models::

    python manage.py syncdb

Or, if you are using South and Django 1.6 or below::

    python manage.py migrate precise_bbcode

The current release of *django-precise-bbcode* supports Django 1.4, 1.5, 1.6 and 1.7. Python 3 is supported.


Built-in BBCodes
----------------

*Django-precise-bbcode* comes with some built-in BBCode tags that you can use to render any content based on bbcodes. The built-in bbcodes are as follows:

+------------+------------------------------+---------------------------------+-------------------------------------+
| BBCode     | Function                     | Options                         | Examples                            |
+============+==============================+=================================+=====================================+
| ``b``      | creates bold text            |                                 | [b]bold text[/b]                    |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``i``      | creates italic text          |                                 | [i]italice text[/i]                 |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``u``      | creates underlined text      |                                 | [u]underlined text[/u]              |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``s``      | creates striked text         |                                 | [s]striked text[/s]                 |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``list``   | creates an unordered list    | 1: ordered list                 | [list][*]one[*]two[/list]           |
|            |                              |                                 |                                     |
|            |                              | 01: ordered list (leading zero) | [list=1][*]one[*]two[/list]         |
|            |                              |                                 |                                     |
|            |                              | a: ordered list (lower alpha)   |                                     |
|            |                              |                                 |                                     |
|            |                              | A: ordered list (upper alpha)   |                                     |
|            |                              |                                 |                                     |
|            |                              | i: ordered list (lower roman)   |                                     |
|            |                              |                                 |                                     |
|            |                              | I: ordered list (upper roman)   |                                     |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``*``      | creates a list item          |                                 | [list][*]one[*]two[/list]           |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``code``   | retains all formatting       |                                 | [code][b]example[/b][/code]         |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``quote``  | creates a blockquote         |                                 | [quote]quoted string[/quote]        |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``center`` | creates a centered block     |                                 | [center]example[/center]            |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``color``  | changes the colour of a text |                                 | [color=red]red text[/color]         |
|            |                              |                                 |                                     |
|            |                              |                                 | [color=#FFFFFF]white text[/color]   |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``url``    | creates a URL                |                                 | [url]http://example.com[/url]       |
|            |                              |                                 |                                     |
|            |                              |                                 | [url=http://example.com]text[/url]  |
+------------+------------------------------+---------------------------------+-------------------------------------+
| ``img``    | displays an image            |                                 | [img]http://xyz.com/logo.png[/img]  |
+------------+------------------------------+---------------------------------+-------------------------------------+

Rendering BBCodes
-----------------

BBcode parser
~~~~~~~~~~~~~

*Django-precise-bbcode* provides a BBCode parser that allows you to transform any textual content containing BBCode tags to the corresponding HTML markup. To do this, just import the ``get_parser`` shortcut and use the ``render`` method of the BBCode parser::

    from precise_bbcode.parser import get_parser

    parser = get_parser()
    rendered = parser.render('[b]Hello [u]world![/u][/b]')

This will store the following HTML into the ``rendered`` variable::

    <strong>Hello <u>world!</u></strong>

Template tags
~~~~~~~~~~~~~

The previous parser can also be used in your templates as a template filter or as a template tag after loading ``bbcode_tags``::

    {% load bbcode_tags %}
    {% bbcode entry.bbcode_content %}
    {{ "[b]Write some bbcodes![/b]"|bbcode }}

Doing this will force the BBCode content included in the ``entry.bbcode_content`` field to be converted to HTML. The last statement will output::

    <strong>Write some bbcodes!</strong>


Storing BBCodes contents
------------------------

The Django built-in ``models.TextField`` is all you need to simply add BBCode contents to your models. However, a common need is to store both the BBCode content and the corresponding HTML markup in the database. To address this *django-precise-bbcode* provides a ``BBCodeTextField``::

    from django.db import models
    from precise_bbcode.fields import BBCodeTextField

    class Post(models.Model):
        content = BBCodeTextField()

A ``BBCodeTextField`` field contributes two columns to the model instead of a standard single column : one is used to save the BBCode content ; the other one keeps the corresponding HTML markup. The HTML content of such a field can then be displayed in any template by using its rendered attribute::

    {{ post.content.rendered }}
