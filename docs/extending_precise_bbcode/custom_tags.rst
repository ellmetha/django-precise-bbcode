##################
Custom BBCode tags
##################

While *django-precise-bbcode* comes with some built-in BBCode tags, there will be times when you need to add your own.

Defining BBCode tags through the admin site
-------------------------------------------

*The easy way.*

*Django-precise-bbcode* provides a ``BBCodeTag`` model which can be seen as a helper to allow end users to easily define BBCode tags. Just go to the admin page and you will see a new 'BBCodes' section. In this section you can create and edit custom BBCode tags. These are then used by the built-in BBCode parser to render any BBCode content.

Adding a custom BBCode tag consists in defining at least two values in the associated admin form, both its usage (tag definition) and its HTML replacement code.

Tag definition
~~~~~~~~~~~~~~~

The tag definition is the expression of the bbcode usage. It's where you enter your bbcode. All you need to do is to add a string containing your BBCode and the associated placeholders (special uppercase words surrounded by { and } -- they are similar to the "replacement fields" that you define in Python format strings)::

    [foo]{TEXT}[/foo]

In this example, we have a bbcode named ``foo`` which can contain some text (``{TEXT}`` placeholder).

So a bbcode definition takes the form of what users will enter when using this bbcode, except that all parts of the bbcode where data is required are expressed as placeholders. The placeholders that you can use in such a tag definition are typed. This means that some semantic verifications are done before rendering in order to ensure that data containing non-allowed characters are not converted to HTML.

*Django-precise-bbcode* provides some placeholders by default, such as ``{TEXT}``, ``{SIMPLETEXT}``, ``{COLOR}``, ``{NUMBER}``, ``{URL}`` or ``{EMAIL}``.  For a full list of the available placeholders and the techniques used to define custom placeholders, please refer to :doc:`custom_placeholders`.

Note that you can specify an option to your bbcode in its definition::

    [foo={COLOR}]{TEXT}[/foo]

In this case, the data associated with the ``{COLOR}`` placeholder is not required at runtime. If you wish to use two placeholders of the same type in your bbcode definition, you have to append a number to their respective names (eg. ``{TEXT1}``)::

    [foo={TEXT1}]{TEXT2}[/foo]

HTML replacement code
~~~~~~~~~~~~~~~~~~~~~

The HTML replacement code is where you enter the HTML for the bbcode you defined previously. All the placeholders you used in your bbcode definition must be present in the HTML replacement code. For example, the HTML replacement code associated with the last ``[foo]`` bbcode example could be::

    <div style="background:{COLOR};">{TEXT}</div>

BBCode options
~~~~~~~~~~~~~~

Some specific options can be used when defining a custom bbcode to alter its default behavior. For example, you could want to forbid the rendering of any bbcode tags included inside your new bbcode. All these options are boolean fields and are indicated in the following table:

+--------------------------+-----------------------------------------------------------------+-------------+
| Option                   | Definition                                                      | Default     |
+==========================+=================================================================+=============+
| newline_closes           | Force the closing of a tag after a newline                      | False       |
+--------------------------+-----------------------------------------------------------------+-------------+
| same_tag_closes          | Force the closing of a tag after the beginning of a similar tag | False       |
+--------------------------+-----------------------------------------------------------------+-------------+
| end_tag_closes           | Force the closing of a tag after the end of another tag         | False       |
+--------------------------+-----------------------------------------------------------------+-------------+
| standalone               | Set this option if a tag does not have a closing tag (eg. [hr]) | False       |
+--------------------------+-----------------------------------------------------------------+-------------+
| transform_newlines       | Convert any line break to the equivalent markup                 | True        |
+--------------------------+-----------------------------------------------------------------+-------------+
| render_embedded          | Force the tags embedded in a tag to be rendered                 | True        |
+--------------------------+-----------------------------------------------------------------+-------------+
| escape_html              | Escape HTML characters (<, >, and &) inside a tag               | True        |
+--------------------------+-----------------------------------------------------------------+-------------+
| replace_links            | Replace URLs with link markups inside a tag                     | True        |
+--------------------------+-----------------------------------------------------------------+-------------+
| strip                    | Strip leading and trailing whitespace inside a tag              | False       |
+--------------------------+-----------------------------------------------------------------+-------------+
| swallow_trailing_newline | Swallow the first trailing newline inside a tag                 | False       |
+--------------------------+-----------------------------------------------------------------+-------------+

Defining BBCode tags plugins
----------------------------

*The fun part.*

While the previous bbcode tag system allows you to easily define various bbcodes, you may want to do more complex treatments with your bbcodes (eg. handle other types of data). You may also want to write some **reusable** or **generic** bbcode tags.

To do so, you will have to write a subclass of ``precise_bbcode.bbcode.tag.BBCodeTag`` for any tag you want to create. These class-based bbcode tags must be defined inside a ``bbcode_tags`` Python module in your Django application (just add a file called ``bbcode_tags.py`` to an existing Django application). And last, but not least, your class-based bbcode tags must be registered to the ``precise_bbcode.tag_pool.tag_pool`` object by using its ``register_tag`` method to be available to the BBCode parser.

Each of these tags must provide a ``name`` attribute and can operate in two different ways:

* The ``BBCodeTag`` subclass provides a ``definition_string`` attribute and a ``format_string`` attribute. In this case, the tag will operate as previously described. The ``definition_string`` corresponds to the tag definition and defines how the tag should be used. The ``format_string`` is the HTML replacement code that will be used to generate the final HTML output
* The ``BBCodeTag`` subclass implements a ``render`` method that will be used to transform the bbcode tag and its context (value, option if provided) to the corresponding  HTML output

Defining bbcodes based on a definition string and a format string
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case, you have to provide a ``definition_string`` attribute and a ``format_string`` attribute to your ``BBCodeTag`` subclass, in addition to the ``name`` attribute.

Let's write a simple example. Consider we are trying to write a ``bar`` bbcode which will strike any text placed inside its tags. So we could write::

    # bbcode_tags.py
    from precise_bbcode.bbcode.tag import BBCodeTag
    from precise_bbcode.tag_pool import tag_pool

    class BarBBCodeTag(BBCodeTag):
        name = 'bar'
        definition_string = '[bar]{TEXT}[/bar]'
        format_string = '<strike>{TEXT}</strike>'

    tag_pool.register_tag(BarBBCodeTag)

Note that you can use any BBCode options specified previously to alter the default behavior of your class-based tags (see `BBCode options`_). To do so, give your bbcode tag options by using an inner class ``Options``, like so::

    # bbcode_tags.py
    from precise_bbcode.bbcode.tag import BBCodeTag
    from precise_bbcode.tag_pool import tag_pool

    class BarBBCodeTag(BBCodeTag):
        name = 'bar'
        definition_string = '[bar]{TEXT}[/bar]'
        format_string = '<strike>{TEXT}</strike>'

        class Options:
            render_embedded = False
            strip = False

    tag_pool.register_tag(BarBBCodeTag)

Defining bbcodes based on a ``render`` method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case, each of your ``BBCodeTag`` subclasses must provide a ``name`` attribute and must implement a ``render`` method. The ``render`` method is used to transform your bbcode tag and its context (value, option if provided) to the corresponding HTML output. The ``render`` method takes three arguments:

* **value**: the context between the start end the end tags, or None for standalone tags. Whether this has been rendered depends on the ``render_embedded`` tag option
* **option**: The value of an option passed to the tag ; defaults to None
* **parent**: The options (instance of ``precise_bbcode.bbcode.tag.BBCodeTagOptions``) associated with the parent bbcode if the tag is being rendered inside another tag, otherwise None

Keep in mind that your ``render`` method may have to validate the data associated with your tag before rendering it. Any validation process should be triggered from this ``render`` method.

Let's write another example. Consider we are trying to write a ``rounded`` bbcode which will surround inside a rounded frame any text placed inside the tags. If provided, the option passed to the tag is assumed to be a colour in order to modify the resulting HTML code. So we could write::

    # bbcode_tags.py
    import re
    from precise_bbcode.bbcode.tag import BBCodeTag
    from precise_bbcode.tag_pool import tag_pool

    color_re = re.compile(r'^([a-z]+|#[0-9abcdefABCDEF]{3,6})$')

    class RoundedBBCodeTag(BBCodeTag):
        name = 'rounded'

        class Options:
            strip = False

        def render(self, value, option=None, parent=None):
            if option and re.search(color_re, option) is not None:
                return '<div class="rounded" style="border-color:{};">{}</div>'.format(option, value)
            return '<div class="rounded">{}</div>'.format(value)

    tag_pool.register_tag(RoundedBBCodeTag)

Again, you can use any BBCode options as previously stated (see `BBCode options`_).

Overriding default BBCode tags
------------------------------

When loaded, the parser provided by *django-precise-bbcode* provides some default bbcode tags (please refer to :doc:`../basic_reference/builtin_bbcodes` for the full list of default tags). These default tags can be overriden. You just have to create another tag with the same name either by defining it in the admin site or by defining it in a ``bbcode_tags`` Python module as previously explained.