Getting started
===============

Requirements
------------

* `Python`_ 2.7, 3.2, 3.3 or 3.4
* `Django`_ 1.4.x, 1.5.x, 1.6.x or 1.7.x
* `Pillow`_ 2.2. or higher
* `South`_ 1.0.1 or higher if you are using Django < 1.7


.. warning:: While *django-precise-bbcode* is compatible with Django 1.5.x, this version of Django
             is no longer supported by the Django team. Please upgrade to
             Django 1.6.x or 1.7.x immediately.

.. _Python: https://www.python.org
.. _Django: https://www.djangoproject.com
.. _Pillow: http://python-pillow.github.io/
.. _South: http://south.aeracode.org/

Installing
----------

Install *django-precise-bbcode* using::

    pip install django-precise-bbcode

Add ``precise_bbcode`` to ``INSTALLED_APPS`` in your project's settings module::

    INSTALLED_APPS = (
        # other apps
        'precise_bbcode',
    )

Then install the models::

    python manage.py syncdb

If you are using Django 1.6 or below, you should use South 1.0 in order to benefit from the migrations. This way you can use the migration command provided by South:

::

  python manage.py migrate precise_bbcode
