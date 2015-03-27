#################################################
Welcome to django-precise-bbcode's documentation!
#################################################

.. image:: http://img.shields.io/pypi/v/django-precise-bbcode.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-precise-bbcode/
    :alt: Latest Version

.. image:: http://img.shields.io/travis/ellmetha/django-precise-bbcode.svg?style=flat-square
    :target: http://travis-ci.org/ellmetha/django-precise-bbcode
    :alt: Build status

.. image:: http://img.shields.io/coveralls/ellmetha/django-precise-bbcode.svg?style=flat-square
    :target: https://coveralls.io/r/ellmetha/django-precise-bbcode
    :alt: Coveralls status

.. image:: http://img.shields.io/pypi/dm/django-precise-bbcode.svg?style=flat-square
    :target: https://pypi.python.org/pypi//django-precise-bbcode/
    :alt: Download

|

**Django-precise-bbcode** is a Django application providing a way to create textual contents based on BBCodes.

  BBCode is a special implementation of HTML. BBCode itself is similar in style to HTML, tags are enclosed in square brackets [ and ] rather than < and > and it offers greater control over what and how something is displayed.

This application includes a BBCode compiler aimed to render any BBCode content to HTML and allows the use of BBCodes tags in models, forms and admin forms. The BBCode parser comes with built-in tags (the default ones ; ``b``, ``u``, ``i``, etc) and allows the definition of custom BBCode tags, placeholders and smilies.

Features
--------

* BBCode parser for rendering any string containing bbcodes
* Tools for handling bbcode contents: templatetags, model field
* Support for custom bbcode tags:

  * Simple custom bbcodes can be defined in the Django admin
  * ... or they can be registered using a plugin system by defining some Python classes
* Support for custom bbcode placeholders
* Support for custom smilies and emoticons


Using django-precise-bbcode
---------------------------

.. toctree::
   :maxdepth: 2

   getting_started
   basic_reference/index
   extending_precise_bbcode/index
   settings


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

