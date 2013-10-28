# -*- coding: utf-8 -*-

# Standard library imports
import re

# Third party imports
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local application / specific library imports
from .parser import bbcodde_standalone_re
from .parser import bbcodde_standard_re


class BBCodeTag(models.Model):
    tag_name = models.SlugField(max_length=20, verbose_name=_('BBCode tag name'), unique=True)
    tag_definition = models.TextField(verbose_name=_('Tag definition'))
    html_replacement = models.TextField(verbose_name=_('Replacement HTML code'))
    helpline = models.CharField(max_length=120, verbose_name=_('Help text for this tag'), null=True, blank=True)
    display_on_editor = models.BooleanField(verbose_name=_('Display on editor'))
    # Tag options
    newline_closes = models.BooleanField(
        verbose_name=_('Newline closing'),
        help_text=_('Set this option to force the closing of this tag after a newline'))
    same_tag_closes = models.BooleanField(
        verbose_name=_('Same tag closing'),
        help_text=_('Set this option to force the closing of this tag after the beginning of a similar tag'))
    standalone = models.BooleanField(
        verbose_name=_('Standalone tag'),
        help_text=_('Set this option if this tag does not have a closing tag'))
    transform_newlines = models.BooleanField(
        verbose_name=_('Transform line breaks'),
        help_text=_('Set this option to convert any line break to the equivalent markup'),
        default=True)
    render_embedded = models.BooleanField(
        verbose_name=('Render embedded tags'),
        help_text=_('Set this option to force the tags embedded in this tag to be rendered'),
        default=True)
    escape_html = models.BooleanField(
        verbose_name=_('Escape HTML characters'),
        help_text=_('Set this option to escape HTML characters (<, >, and &) inside this tag'),
        default=True)
    replace_links = models.BooleanField(
        verbose_name=_('Replace links'),
        help_text=_('Set this option to replace URLs with link markups inside this tag'),
        default=True)
    strip = models.BooleanField(
        verbose_name=_('Strip leading and trailing whitespace'),
        help_text=_('Set this option to strip leading and trailing whitespace inside this tag'))
    swallow_trailing_newline = models.BooleanField(
        verbose_name=_('Swallow trailing newline'),
        help_text=_('Set this option to swallow the first trailing newline'))

    class Meta:
        verbose_name = _('BBCode tag')
        verbose_name_plural = _('BBCode tags')
        app_label = 'precise_bbcode'

    def __unicode__(self):
        return u'%s' % (self.tag_name)

    def clean(self):
        tag_re = bbcodde_standard_re if not self.standalone else bbcodde_standalone_re
        valid_bbcode_tag = re.search(tag_re, self.tag_definition)
        # First, try to validate the tag according to the correct regex
        if not valid_bbcode_tag:
            raise ValidationError(_("The BBCode definition you provided is not valid"))
        re_groups = re.search(tag_re, self.tag_definition).groupdict()
        # The beginning and end tag names must be the same
        if not self.standalone and re_groups['start_name'] != re_groups['end_name']:
            raise ValidationError(_("This BBCode tag dit not validate because the start tag and the tag names are not the same"))
        # The tag name must be unique
        if BBCodeTag.objects.filter(tag_name=re_groups['start_name']).exists():
            raise ValidationError(_("A BBCode tag with this name appears to already exist"))
        super(BBCodeTag, self).clean()

    def save(self, *args, **kwargs):
        tag_re = bbcodde_standard_re if not self.standalone else bbcodde_standalone_re
        # Generate the tag name according to the tag definition
        re_groups = re.search(tag_re, self.tag_definition).groupdict()
        self.tag_name = re_groups['start_name']

        super(BBCodeTag, self).save(*args, **kwargs)
