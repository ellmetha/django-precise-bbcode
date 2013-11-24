# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import re

# Third party imports
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local application / specific library imports
from .parser import bbcodde_standalone_re
from .parser import bbcodde_standard_re
from .parser import BBCodeParser
from .parser import BBCodeTagOptions
from .parser import get_parser
from .parser import placeholder_re


class BBCodeTag(models.Model):
    tag_name = models.SlugField(max_length=20, verbose_name=_('BBCode tag name'), unique=True)
    tag_definition = models.TextField(verbose_name=_('Tag definition'))
    html_replacement = models.TextField(verbose_name=_('Replacement HTML code'))
    helpline = models.CharField(max_length=120, verbose_name=_('Help text for this tag'), null=True, blank=True)
    display_on_editor = models.BooleanField(verbose_name=_('Display on editor'), default=True)
    # Tag options
    newline_closes = models.BooleanField(
        verbose_name=_('Newline closing'),
        help_text=_('Set this option to force the closing of this tag after a newline'),
        default=False)
    same_tag_closes = models.BooleanField(
        verbose_name=_('Same tag closing'),
        help_text=_('Set this option to force the closing of this tag after the beginning of a similar tag'),
        default=False)
    end_tag_closes = models.BooleanField(
        verbose_name=_('End tag closing'),
        help_text=_('Set this option to force the closing of this tag after the end of another tag'),
        default=False)
    standalone = models.BooleanField(
        verbose_name=_('Standalone tag'),
        help_text=_('Set this option if this tag does not have a closing tag'),
        default=False)
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
        help_text=_('Set this option to strip leading and trailing whitespace inside this tag'),
        default=False)
    swallow_trailing_newline = models.BooleanField(
        verbose_name=_('Swallow trailing newline'),
        help_text=_('Set this option to swallow the first trailing newline'),
        default=False)

    class Meta:
        verbose_name = _('BBCode tag')
        verbose_name_plural = _('BBCode tags')
        app_label = 'precise_bbcode'

    def __unicode__(self):
        return '{}'.format(self.tag_name)

    def clean(self):
        parser = get_parser()

        tag_re = bbcodde_standard_re if not self.standalone else bbcodde_standalone_re
        valid_bbcode_tag = re.search(tag_re, self.tag_definition)

        # First, try to validate the tag according to the correct regex
        if not valid_bbcode_tag:
            raise ValidationError(_("The BBCode definition you provided is not valid"))
        re_groups = re.search(tag_re, self.tag_definition).groupdict()

        # The beginning and end tag names must be the same
        if not self.standalone and re_groups['start_name'] != re_groups['end_name']:
            raise ValidationError(_("This BBCode tag dit not validate because the start tag and the tag names are not the same"))

        if re_groups['start_name'] in parser.bbcodes.keys():
            raise ValidationError(_("A BBCode tag with this name appears to already exist"))

        # The used placeholders must be the same in the tag definition and in the HTML replacement code
        def_placeholders = re.findall(placeholder_re, self.tag_definition)
        html_placeholders = re.findall(placeholder_re, self.html_replacement)
        if set(def_placeholders) != set(html_placeholders):
            raise ValidationError(_("The placeholders defined in the tag definition must be present in the HTML replacement code!"))

        # ... and two placeholders must not have the same name
        def_placeholders_uniques = list(set(def_placeholders))
        if def_placeholders != sorted(def_placeholders_uniques):
            raise ValidationError(_("The placeholders defined in the tag definition must be strictly uniques"))

        # Moreover, the used placeholders must be known by the BBCode parser and they must have the same name,
        # with some variations: eg {TEXT} can be used as {TEXT1} or {TEXT2} if two 'TEXT' placeholders are needed
        placeholder_types = [re.sub('\d+$', '', placeholder) for placeholder in def_placeholders]
        valid_placeholder_types = [placeholder for placeholder in placeholder_types if placeholder in BBCodeParser.PLACEHOLDERS_RE.keys()]
        if valid_placeholder_types != placeholder_types:
            raise ValidationError(_("You can only use placeholder names among: " + str(BBCodeParser.PLACEHOLDERS_RE.keys())
                                  + ". If you need many placeholders of a specific type, you can append numbers to them (eg. {TEXT1} or {TEXT2})"))

        super(BBCodeTag, self).clean()

    def save(self, *args, **kwargs):
        tag_re = bbcodde_standard_re if not self.standalone else bbcodde_standalone_re
        # Generate the tag name according to the tag definition
        re_groups = re.search(tag_re, self.tag_definition).groupdict()
        self.tag_name = re_groups['start_name']

        super(BBCodeTag, self).save(*args, **kwargs)

    @property
    def parser_args(self):
        """
        Returns a tuple of the form: (args, kwargs). This is aimed to be used as arguments for adding the current tag
        to the tags list of a BBCode parser.
        """
        # Constructs the positional arguments list
        args = [self.tag_name, self.tag_definition, self.html_replacement]
        # Constructs the keyword arguments dict
        kwargs = {}
        opts = self._meta
        tag_option_attrs = vars(BBCodeTagOptions)
        for f in opts.fields:
            if f.name in tag_option_attrs:
                kwargs[f.name] = f.value_from_object(self)

        return (args, kwargs)
