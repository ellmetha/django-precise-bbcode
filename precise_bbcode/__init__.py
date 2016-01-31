# -*- coding: utf-8 -*-

default_app_config = 'precise_bbcode.apps.PreciseBbCodeAppConfig'

pkg_resources = __import__('pkg_resources')
distribution = pkg_resources.get_distribution('django-precise-bbcode')
__version__ = distribution.version
