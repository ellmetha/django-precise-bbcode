# -*- coding: utf-8 -*-

from django import VERSION
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if VERSION >= (1, 8):
    patterns = lambda _, *p: list(p)
else:
    from django.conf.urls import patterns


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
