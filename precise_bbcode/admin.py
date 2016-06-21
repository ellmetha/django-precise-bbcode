# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import actions
from django.utils.translation import ugettext_lazy as _

from .bbcode import get_parser
from .models import BBCodeTag
from .models import SmileyTag


class BBCodeTagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'tag_definition', 'html_replacement')
    list_display_links = ('tag_name', 'tag_definition', 'html_replacement')
    fieldsets = (
        (None, {
            'fields': (
                'tag_definition', 'html_replacement', 'helpline', 'standalone', 'display_on_editor')
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'newline_closes',
                'same_tag_closes',
                'end_tag_closes',
                'transform_newlines',
                'render_embedded',
                'escape_html',
                'replace_links',
                'strip',
                'swallow_trailing_newline'
            )
        }),
    )

    def get_actions(self, request):
        actions = super(BBCodeTagAdmin, self).get_actions(request)
        actions['delete_selected'] = (
            BBCodeTagAdmin.delete_selected,
            'delete_selected',
            _('Delete selected %(verbose_name_plural)s'),
        )
        return actions

    def delete_selected(self, request, queryset):
        parser = get_parser()
        tag_names = list(queryset.values_list('tag_name', flat=True))
        response = actions.delete_selected(self, request, queryset)

        if response is None:
            [parser.bbcodes.pop(n) for n in tag_names]

        return response


class SmileyTagAdmin(admin.ModelAdmin):
    list_display = ('code', 'emotion')
    list_display_links = ('code', 'emotion')


admin.site.register(BBCodeTag, BBCodeTagAdmin)
admin.site.register(SmileyTag, SmileyTagAdmin)
