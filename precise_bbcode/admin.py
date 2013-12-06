# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Local application / specific library imports
from .models import BBCodeTag
from .models import SmileyTag


class BBCodeTagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'tag_definition', 'html_replacement')
    list_display_links = ('tag_name', 'tag_definition', 'html_replacement')
    fieldsets = (
        (None, {
            'fields': ('tag_definition', 'html_replacement', 'helpline', 'standalone', 'display_on_editor')
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


class SmileyTagAdmin(admin.ModelAdmin):
    list_display = ('code', 'emotion')
    list_display_links = ('code', 'emotion')


admin.site.register(BBCodeTag, BBCodeTagAdmin)
admin.site.register(SmileyTag, SmileyTagAdmin)
