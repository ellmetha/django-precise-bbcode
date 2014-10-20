##########################
Custom BBCode placeholders
##########################

When you define bbcode tags, you can choose to use placeholders in order to define where data is required. These placeholders, such as ``{TEXT}`` or ``{NUMBER}`` are typed.  This means that some semantic verifications are done before rendering in order to ensure that data corresponding to a specific placeholder is valid. *Django-precise-bbcode* comes with some built-in BBCode placeholders that you can use in your bbcode tag definitions. You can also choose to create your owns.

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

