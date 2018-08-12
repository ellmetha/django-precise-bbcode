Getting started
===============

Requirements
------------

* `Python`_ 2.7, 3.4, 3.5, 3.6 or 3.7
* `Django`_ 1.11.x, 2.0.x or 2.1.x
* `Pillow`_ 2.2. or higher

.. _Python: https://www.python.org
.. _Django: https://www.djangoproject.com
.. _Pillow: http://python-pillow.github.io/

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

    python manage.py migrate
