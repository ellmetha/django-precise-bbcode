# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import TestMessage


class TestMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'bbcode_content')
    list_display_links = ('id', 'bbcode_content')
    fields = ('bbcode_content', )


admin.site.register(TestMessage, TestMessageAdmin)
