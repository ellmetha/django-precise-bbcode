=====================
django-precise-bbcode
=====================

.. image:: https://pypip.in/version/django-precise-bbcode/badge.png
    :target: https://pypi.python.org/pypi/django-precise-bbcode/
    :alt: Latest Version

.. image:: https://travis-ci.org/ellmetha/django-precise-bbcode.svg?branch=master
    :target: https://travis-ci.org/ellmetha/django-precise-bbcode
    :alt: Travis status

.. image:: https://coveralls.io/repos/ellmetha/django-precise-bbcode/badge.png?branch=master
    :target: https://coveralls.io/r/ellmetha/django-precise-bbcode
    :alt: Coveralls status

.. image:: https://pypip.in/download/django-precise-bbcode/badge.png
    :target: https://pypi.python.org/pypi//django-precise-bbcode/
    :alt: Download

.. image:: https://pypip.in/wheel/django-precise-bbcode/badge.png
    :target: https://pypi.python.org/pypi/django-precise-bbcode/
    :alt: Wheel Status

|
*Django-precise-bbcode* is a Django application providing a way to create textual contents based on BBCodes.

  BBCode is a special implementation of HTML. BBCode itself is similar in style to HTML, tags are enclosed in square brackets [ and ] rather than < and > and it offers greater control over what and how something is displayed.

This application includes a BBCode compiler aimed to render any BBCode content to HTML and allows the use of BBCodes tags in models, forms and admin forms. The BBCode parser comes with built-in tags (the default ones ; ``b``, ``u``, etc) and allows the use of smilies and custom BBCode tags. These can be added in two different ways:

* Custom tags can be defined in the Django administration panel and stored into the database ; doing this allows any non-technical admin to add BBCode tags by defining the HTML replacement string associated with each tag
* Tags can also be manually registered to be used by the parser by defining a tag class aimed to render a given bbcode tag and its content to the corresponding HTML markup

Read more in the `documentation <http://django-precise-bbcode.readthedocs.org/en/latest/>`_ (latest version).

Requirements
------------

* ``python >= 2.7`` (tested with version 2.7, 3.2, 3.3, 3.4)
* ``django >= 1.4.2`` (tested with version 1.4.2, 1.5, 1.6, 1.7)
* ``PIL`` or ``Pillow`` (required for smiley tags)
* ``setuptools``


Installation
------------

Just run:

::

  pip install django-precise-bbcode
  
Once installed you can configure your project to use *django-precise-bbcode* with the following steps.

Add ``precise_bbcode`` to ``INSTALLED_APPS`` in your project's settings module:

::

  INSTALLED_APPS = (
      # other apps
      'precise_bbcode',
  )

Then install the models:

::

  python manage.py syncdb

If you are using South **and** Django 1.6 or below you have to customize the ``SOUTH_MIGRATION_MODULES`` setting as follow:

::

  SOUTH_MIGRATION_MODULES = {
      'precise_bbcode': 'precise_bbcode.south_migrations',
  }

Then you can use the migration command provided by South:

::

  python manage.py migrate precise_bbcode


Usage
-----

Rendering bbcodes
*****************

*Django-precise-bbcode* comes with a BBCode parser that allows you to transform a textual content containing BBCode tags to the corresponding HTML markup. To do this, simply import the ``get_parser`` shortcut and use the ``render`` method of the BBCode parser::

  >>> from precise_bbcode.parser import get_parser
  >>> parser = get_parser()
  >>> parser.render('[b]Hello [u]world![/u][/b]')
  '<strong>Hello <u>world!</u></strong>'

*It's that easy!*

As you may need to render bbcodes inside one of your Django template, this parser can be used as a template filter or as a template tag after loading ``bbcode_tags``::

  {% load bbcode_tags %}
  {% bbcode entry.bbcode_content %}
  {{ "[b]Write some bbcodes![/b]"|bbcode }}

The BBCode content included in the ``entry.bbcode_content``  field will be converted to HTML and displayed. The last statement will output ``<strong>Write some bbcodes!</strong>``.

Storing bbcodes
***************

While you can use the Django built-in ``models.TextField`` to add your BBCode contents to your models, a common need is to store both the BBCode content and the corresponding HTML markup in the database. To address this *django-precise-bbcode* provides a ``BBCodeTextField``.

::
  
  from django.db import models
  from precise_bbcode.fields import BBCodeTextField

  class Post(models.Model):
      content = BBCodeTextField()

This field will store both the BBCode content and the correspondign HTML markup. The HTML content of such a field can then be displayed in any template by using its ``rendered`` attribute:

::

  {{ post.content.rendered }}

And more...
***********

Head over to the `documentation <http://django-precise-bbcode.readthedocs.org/en/latest/>`_ for all the details on how to use the BBCode parser and how to define custom BBcode tags and smilies.

Author
------

Morgan Aubert (@ellmetha) <morgan.aubert@zoho.com>

License
-------

BSD. See ``LICENSE`` for more details.
