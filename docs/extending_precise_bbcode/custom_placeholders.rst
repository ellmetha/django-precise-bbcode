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