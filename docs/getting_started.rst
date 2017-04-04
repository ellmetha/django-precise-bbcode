Getting started
===============

Requirements
------------

* `Python`_ 2.7, 3.3, 3.4 or 3.5
* `Django`_ 1.8.x, 1.9.x, 1.10.x or 1.11.x
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
