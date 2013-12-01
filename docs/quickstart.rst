Quickstart
===========

Install the project using::

    pip install django-precise-bbcode

Add ``precise_bbcode`` to ``INSTALLED_APPS`` in your project's settings module:::

    INSTALLED_APPS += (
        # other apps
        'precise_bbcode',
    )

The current release of *django-precise-bbcode* supports Django 1.4, 1.5 and 1.6. Python 3 is supported.


Built-in BBCodes
----------------

*Django-precise-bbcode* comes with some built-in BBCode tags that you can use to render any content based on bbcodes. The built-in bbcodes are as follows:

+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| BBCode      | Function                                      | Options                         | Examples                            |
+=============+===============================================+=================================+=====================================+
| ``b``       | creates bold text                             |                                 | [b]bold text[/b]                    |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``i``       | creates italic text                           |                                 | [i]italice text[/i]                 |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``u``       | creates underlined text                       |                                 | [u]underlined text[/u]              |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``s``       | creates striked text                          |                                 | [s]striked text[/s]                 |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``list``    | creates an unordered list                     | 1: ordered list                 | [list][*]one[*]two[/list]           |
|             |                                               | 01: ordered list (leading zero) |                                     |
|             |                                               | a: ordered list (lower alpha)   | [list=1][*]one[*]two[/list]         |
|             |                                               | A: ordered list (upper alpha)   |                                     |
|             |                                               | i: ordered list (lower roman)   |                                     |
|             |                                               | I: ordered list (upper roman)   |                                     |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``*``       | creates a list item                           |                                 | [list][*]one[*]two[/list]           |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``code``    | retains all formatting used within this ta    |                                 | [code][b]example[/b][/code]         |
|             | when it is displayed                          |                                 |                                     |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``quote``   | creates a blockquote                          |                                 | [quote]quoted string[/quote]        |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``center``  | creates a centered block of text              |                                 | [center]example[/center]            |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``color``   | changes the colour of a text                  |                                 | [color=red]red text[/color]         |
|             |                                               |                                 |                                     |
|             |                                               |                                 | [color=#FFFFFF]white text[/color]   |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``url``     | creates a URL                                 |                                 | [url]http://example.com[/url]       |
|             |                                               |                                 |                                     |
|             |                                               |                                 | [url=http://example.com]text[/url]  |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+
| ``img``     | displays an image                             |                                 | [img]http://xyz.com/logo.png[/img]  |
+-------------+-----------------------------------------------+---------------------------------+-------------------------------------+

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
