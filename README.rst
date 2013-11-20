django-precise-bbcode
=====================

**Django-precise-bbcode** is a Django application providing a way to create textual contents based on BBCodes.

  BBCode is a special implementation of HTML. BBCode itself is similar in style to HTML, tags are enclosed in square brackets [ and ] rather than < and > and it offers greater control over what and how something is displayed.

This application includes a BBCode compiler aimed to render any BBCode content to HTML and allows the use of BBCodes tags in models, forms and admin forms. The BBCode parser comes with built-in tags (the default ones ; ``b``, ``u``, etc) and allows the use of custom BBCode tags. These can be added in two different ways:

* Custom tags can be defined in the Django administration panel and stored into the database ; doing this allows any non-technical admin to add BBCode tags by defining the HTML replacement string associated with each tag
* Tags can also be manually registered to be used by the parser by defining a tag class aimed to render a given bbcode tag and its content to the corresponding HTML markup

Requirements
------------

* ``python >= 2.7`` (tested with version 2.7, 3.2)
* ``django >= 1.4`` (tested with version 1.4, 1.5, 1.6)
* ``setuptools``


Installation
------------

Just run:

::

  pip install git+git://github.com/ellmetha/django-precise-bbcode.git#egg=django-precise-bbcode

Once installed you can configure your project to use django-precise-bbcode with the following steps.

Add ``precise_bbcode`` to ``INSTALLED_APPS`` in your project's settings module:

::

  INSTALLED_APPS = (
      # other apps
      'precise_bbcode',
  )

Then install the models:

::

  python manage.py syncdb      # Or python manage.py migrate precise_bbcode if you are using South

Usage
-----

Rendering tools
***************

Templatetags
~~~~~~~~~~~~

Django-precise-bbcode comes with a BBCode parser that allows you to transform a textual content containing BBCode tags to the corresponding HTML markup. This parser can be used in your templates as a template filter or as a template tag after loading ``bbcode_tags``:

::

  {% load bbcode_tags %}
  {% bbcode entry.bbcode_content %}
  {{ "[b]Write some bbcodes![/b]"|bbcode }}

The BBCode content included in the ``entry.bbcode_content``  field will be converted to HTML. The last statement will output ``<strong>Write some bbcodes!</strong>``.

BBCode parser
~~~~~~~~~~~~~

The BBCode parser built in Django-precise-bbcode can also be used if you need to convert BBCode contents to HTML outside of Django templates. Just use the ``render`` method of the BBCode parser:

::

  from precise_bbcode.parser import get_parser
  
  parser = get_parser()
  parser.render('[b]Hello [u]world![/u][/b]')

BBCode fields
-------------

The Django built-in ``models.TextField`` is all you need to simply add BBCode contents to your models. However, a common need is to store both the BBCode content and the corresponding HTML markup in the database. To address this Django-precise-bbcode provides a ``BBCodeTextField``.

::
  
  from django.db import models
  from precise_bbcode.fields import BBCodeTextField

  class Post(models.Model):
      content = BBCodeTextField()

A ``BBCodeTextField`` field contributes two columns to the model instead of a standard single column : one is used to save the BBCode content ; the other one keeps the corresponding HTML markup. The HTML content of such a field can then be displayed in any template by using its ``rendered`` attribute:

::

  {{ post.content.rendered }}

Custom BBCode tags
------------------

While Django-precise-bbcode comes with some built-in BBCode tags, there will be times when you need to add your own.

The easiest way to add a custom tag is to define it by using the Django administration system. Just got to the admin page and you will see a new 'BBCode tags' section. In this you can create and edit custom BBCode tags. These are then used by the built-in BBCode parser to render any BBCode content. Adding such a custom BCode tag consists in defining at least two values in the associated admin form:

* The definition of the tag: it's wehere you enter your BBCode. All you need to do is to add a string containing your BBCode and the associated placeholders (special uppercase words surrounded by { and } -- they are similar to the "replacement fields" that you define in python format strings). For example, you would enter the following string for a very simple ``[red]`` bbcode:

  ::

    [red]{TEXT}[/red]

  The placeholders that you can use in the tag definition are typed. Only the following placeholders can be used: ``TEXT``, ``SIMPLETEXT``, ``URL``, ``EMAIL``, ``COLOR``, ``NUMBER``.
* The HTML replacement code: you will enter the HTML for the BBCode you defined previously. All the placeholders you used in your BBCode definition must be replaced in the HTML replacement code. For example, the HTML replacement code associated with the previous ``[red]`` bbcode can be:

  ::
    
    <span style="color:red;">{TEXT}</span>

For defining more complex BBCodes, it is also possible to add class-based BBCodes inside a ``bbcode_tags`` module in each Django application. These must provide a ``render`` method and must be registered to a tag pool in order to be available to the BBCode parser. The previous ``[red]`` BBCode could be converted to such a class-based tag as follows:

::

  from precise_bbcode.tag_base import TagBase
  from precise_bbcode.tag_pool import tag_pool
  
  class RedTag(TagBase):
      tag_name = "red"
    
      def render(self, name, value, option=None, parent=None):
          return '<span style="color:red;">%s</span>' % value

  tag_pool.register_tag(RedTag)

Author
------

Morgan Aubert (@ellmetha) <morgan.aubert@zoho.com>

License
-------

BSD. See ``LICENSE`` for more details.
