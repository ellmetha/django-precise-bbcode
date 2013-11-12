django-precise-bbcode
=====================

**Django-precise-bbcode** is a Django application providing a way to create textual contents based on BBCodes.

  BBCode is a special implementation of HTML. BBCode itself is similar in style to HTML, tags are enclosed in square brackets [ and ] rather than < and > and it offers greater control over what and how something is displayed.

This application includes a BBCode compiler aimed to render any BBCode content to HTML and allows the use of BBCodes tags in models, forms and admin forms. The BBCode parser comes with built-in tags (the default ones ; ``b``, ``u``, etc) and allows the use of custom BBCode tags. These can be added in two different ways:

* Custom tags can be defined in the Django administration panel and stored into the database ; doing this allows any non-technical admin to add BBCode tags by defining the HTML replacement string associated with each tag
* Tags can also be manually registered to be used by the parser by defining a tag class aimed to render a given bbcode tag and its content to the corresponding HTML markup

*Note that django-precise-bbcode is in an early stage of development*

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

  python manage.py syncdb      # Or python migrate precise_bbcode if you are using South

Author
------

Morgan Aubert (@ellmetha) <morgan.aubert@zoho.com>

License
-------

BSD. See ``LICENSE`` for more details.
