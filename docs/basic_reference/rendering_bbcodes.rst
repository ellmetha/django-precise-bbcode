#################
Rendering BBCodes
#################

BBcode parser
-------------

*Django-precise-bbcode* provides a BBCode parser that allows you to transform any textual content containing BBCode tags to the corresponding HTML markup. To do this, just import the ``get_parser`` shortcut and use the ``render`` method of the BBCode parser::

    from precise_bbcode.bbcode import get_parser

    parser = get_parser()
    rendered = parser.render('[b]Hello [u]world![/u][/b]')

This will store the following HTML into the ``rendered`` variable::

    <strong>Hello <u>world!</u></strong>

Template tags
-------------

The previous parser can also be used in your templates as a template filter or as a template tag after loading ``bbcode_tags``::

    {% load bbcode_tags %}
    {% bbcode entry.bbcode_content %}
    {{ "[b]Write some bbcodes![/b]"|bbcode }}

Doing this will force the BBCode content included in the ``entry.bbcode_content`` field to be converted to HTML. The last statement will output::

    <strong>Write some bbcodes!</strong>

Jinja2 template support
-----------------------

*Django-precise-bbcode* supports Jinja 2 templating. You have to add the ``precise_bbcode.jinja2tags.bbcode`` extension to your template extensions if you want to use the *django-precise-bbcode*'s Jinja 2 tags in your project::

    TEMPLATES = [
        # ...
        {
            'BACKEND': 'django.template.backends.jinja2.Jinja2',
            'APP_DIRS': True,
            'OPTIONS': {
                'extensions': [
                    'precise_bbcode.jinja2tags.bbcode',
                ],
            },
        }
    ]

The BBCode parser can then be used into your Jinja 2 templates as a function or as a template filter::

    {{ bbcode("[b]Write some bbcodes![/b]") }}
    {{ "[b]Write some bbcodes![/b]"|bbcode }}
