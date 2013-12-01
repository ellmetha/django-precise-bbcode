Welcome to django-precise-bbcode's documentation!
=================================================

.. image::  https://travis-ci.org/ellmetha/django-precise-bbcode.png?branch=master
  :target: http://travis-ci.org/ellmetha/django-precise-bbcode
  :alt: build-status
.. image:: https://coveralls.io/repos/ellmetha/django-precise-bbcode/badge.png?branch=master
  :target: https://coveralls.io/r/ellmetha/django-precise-bbcode?branch=master 

|

**Django-precise-bbcode** is a Django application providing a way to create textual contents based on BBCodes.

  BBCode is a special implementation of HTML. BBCode itself is similar in style to HTML, tags are enclosed in square brackets [ and ] rather than < and > and it offers greater control over what and how something is displayed.

This application includes a BBCode compiler aimed to render any BBCode content to HTML and allows the use of BBCodes tags in models, forms and admin forms. The BBCode parser comes with built-in tags (the default ones ; ``b``, ``u``, ``i``, etc) and allows the definition of custom BBCode tags.

Features
--------

* BBCode parser for rendering any string containing bbcodes
* Tools for handling bbcode contents: templatetags, model field
* Support for custom bbcode tags:

  * Simple custom bbcodes can be defined in the Django admin
  * ... or they can be registered using a plugin system by defining some Python classes


Using django-precise-bbcode
---------------------------

.. toctree::
   :maxdepth: 2

   quickstart
   custom_tags


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

