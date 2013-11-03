# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.contrib import admin

# Local application / specific library imports
from .models import TestMessage


class TestMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'bbcode_content')
    list_display_links = ('id', 'bbcode_content')
    fields = ('bbcode_content', )

admin.site.register(TestMessage, TestMessageAdmin)
