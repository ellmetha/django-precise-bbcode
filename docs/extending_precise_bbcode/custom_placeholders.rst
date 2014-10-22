##########################
Custom BBCode placeholders
##########################

When you define bbcode tags, you can choose to use placeholders in order to define where data is required. These placeholders, such as ``{TEXT}`` or ``{NUMBER}`` are typed.  This means that some semantic verifications are done before rendering in order to ensure that the content corresponding to a specific placeholder is valid. *Django-precise-bbcode* comes with some built-in BBCode placeholders that you can use in your bbcode tag definitions. You can also choose to create your owns.

Built-in placeholders
---------------------

+-----------------+---------------------+--------------------------------------------------+
| Placeholder     | Usage               | Definition                                       |
+=================+=====================+==================================================+
| ``{TEXT}``      |                     | matches anything                                 |
+-----------------+---------------------+--------------------------------------------------+
| ``{SIMPLETEXT}``|                     | matches latin characters, numbers, spaces,       |
|                 |                     |                                                  |
|                 |                     | commas, dots, minus, plus, hyphen and underscore |
+-----------------+---------------------+--------------------------------------------------+
| ``{COLOR}``     |                     | matches a colour (eg. ``red`` or ``#000FFF``)    |
+-----------------+---------------------+--------------------------------------------------+
| ``{NUMBER}``    |                     | matches a number                                 |
+-----------------+---------------------+--------------------------------------------------+
| ``{URL}``       |                     | matches a valid URL                              |
+-----------------+---------------------+--------------------------------------------------+
| ``{EMAIL}``     |                     | matches a valid e-mail address                   |
+-----------------+---------------------+--------------------------------------------------+
| ``{RANGE}``     | ``{RANGE=min,max}`` | matches a valid number between *min* and *max*   |
+-----------------+---------------------+--------------------------------------------------+
| ``{CHOICE}``    | ``{CHOICE=foo,bar}``| matches all strings separated with commas in the |
|                 |                     |                                                  |
|                 |                     | placeholder                                      |
+-----------------+---------------------+--------------------------------------------------+

Defining BBCode placeholders plugins
------------------------------------

*Django-precise-bbcode* allows you to define your own placeholders.

To do so, you will have to write a subclass of ``precise_bbcode.bbcode.placeholder.BBCodePlaceholder`` for any placeholder you want to create. These class-based bbcode placeholders must be defined inside a ``bbcode_placeholders`` Python module in your Django application (just add a file called ``bbcode_placeholders.py`` to an existing Django application). In the same way as bbcode tag classes, your class-based bbcode placeholders must be registered to the ``precise_bbcode.placeholder_pool.placeholder_pool`` object by using its ``register_placeholder`` method to be available to the BBCode parser.

Each bbcode placeholder must have a ``name`` attribute and can operate in two different ways:

* The ``BBCodePlaceholder`` subclass provides a ``pattern`` attribute, which is a valid regular expression. In this case, a given content will be valid in the context of the placeholder if it match this regular expression
* The ``BBCodePlaceholder`` subclass implements a ``validate`` method. This method is used to check whether a given content is valid according to the placeholder definition associated to it

Defining placeholders based on a regular expression pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case, you have to provide a ``pattern`` attribute to your ``BBCodePlaceholder`` subclass, in addition to the ``name`` attribute.

Let's write a simple example. Consider we are trying to write a ``{PHONENUMBER}`` bbcode placeholder which will allow end-users to fill some bbcode tags with phone numbers. So we could write::

    # bbcode_placeholders.py
    import re
    from precise_bbcode.bbcode.placeholder import BBCodePlaceholder
    from precise_bbcode.placeholder_pool import placeholder_pool

    class PhoneNumberBBCodePlaceholder(BBCodePlaceholder):
        name = 'phonenumber'
        pattern = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')

    placeholder_pool.register_placeholder(PhoneNumberBBCodePlaceholder)

So if this placeholder is used inside, let's say, a ``[telto]`` bbcode tag, ``+33000000000`` will be a valid input.

Defining placeholders based on a ``validate`` method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case, each of your ``BBCodePlaceholder`` subclasses must provide a ``name`` attribute and must implement a ``validate`` method. This method is used to check whether the input associated with a placeholder is valid and can be rendered. The ``validate`` method takes two arguments:

* **content**: the content used to fill the placeholder that must be validated
* **extra_context**: the extra context of the placeholder if defined in a tag definition

Note that the extra context is a string defined in the placeholder in a bbcode tag definition. For example, ``CHOICE`` is the placeholder name and ``apple,tomato`` is the extra context if the ``CHOICE`` placeholder is used as follows inside a bbcode tag definition: ``{CHOICE=apple,tomato}``.

Let's write an example. Consider we are trying to write a ``{RANGE}`` placeholder which will allow end-users to fill some bbcode tags with a number that will be valid only if it is within a specific range. So we could write::

    # bbcode_placeholders.py
    import re
    from precise_bbcode.bbcode.placeholder import BBCodePlaceholder
    from precise_bbcode.placeholder_pool import placeholder_pool

    class RangeBBCodePlaceholder(BBCodePlaceholder):
        name = 'range'

        def validate(self, content, extra_context):
            try:
                value = float(content)
            except ValueError:
                return False

            try:
                min_content, max_content = extra_context.split(',')
                min_value, max_value = float(min_content), float(max_content)
            except ValueError:
                return False

            if not (value >= min_value and value <= max_value):
                return False

        return True


    placeholder_pool.register_placeholder(RangeBBCodePlaceholder)

The ``validate`` method allows you to implement your own validation logic for your custom placeholders.

Overriding default BBCode placeholders
--------------------------------------

When loaded, the parser provided by *django-precise-bbcode* provides some default bbcode placeholders (please refer to `Built-in placeholders`_ for the full list of default placeholders). These default placeholders can be overridden. You just have to register another placeholder with the same name and it will override the default one.