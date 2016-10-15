# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import force_str
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .bbcode import get_parser
from .bbcode.regexes import bbcodde_standalone_re
from .bbcode.regexes import bbcodde_standard_re
from .bbcode.regexes import placeholder_content_re
from .bbcode.regexes import placeholder_re
from .bbcode.tag import BBCodeTag as ParserBBCodeTag
from .bbcode.tag import BBCodeTagOptions
from .conf import settings as bbcode_settings
from .fields import SmileyCodeField


@python_2_unicode_compatible
class BBCodeTag(models.Model):
    tag_name = models.SlugField(max_length=20, verbose_name=_('BBCode tag name'), unique=True)
    tag_definition = models.TextField(verbose_name=_('Tag definition'))
    html_replacement = models.TextField(verbose_name=_('Replacement HTML code'))

    # Tag options
    newline_closes = models.BooleanField(
        verbose_name=_('Newline closing'),
        help_text=_('Set this option to force the closing of this tag after a newline'),
        default=False)
    same_tag_closes = models.BooleanField(
        verbose_name=_('Same tag closing'),
        help_text=_('Set this option to force the closing of this tag after the '
                    'beginning of a similar tag'),
        default=False)
    end_tag_closes = models.BooleanField(
        verbose_name=_('End tag closing'),
        help_text=_('Set this option to force the closing of this tag after the end '
                    'of another tag'),
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
        verbose_name=_('Render embedded tags'),
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

    # For later use
    helpline = models.CharField(
        max_length=120, verbose_name=_('Help text for this tag'), null=True, blank=True)
    display_on_editor = models.BooleanField(verbose_name=_('Display on editor'), default=True)

    class Meta:
        verbose_name = _('BBCode tag')
        verbose_name_plural = _('BBCode tags')
        app_label = 'precise_bbcode'

    def __str__(self):
        return '{}'.format(self.tag_name)

    def clean(self):
        old_instance = None
        if self.pk:
            old_instance = self.__class__._default_manager.get(pk=self.pk)

        parser = get_parser()

        tag_re = bbcodde_standard_re if not self.standalone else bbcodde_standalone_re
        valid_bbcode_tag = re.search(tag_re, self.tag_definition)
        def_placeholders = re.findall(placeholder_re, self.tag_definition)

        # First, try to validate the tag according to the correct regex
        if not valid_bbcode_tag:
            raise ValidationError(_('The BBCode definition you provided is not valid'))
        re_groups = re.search(tag_re, self.tag_definition).groupdict()

        # Validates the tag definition by trying to create the corresponding BBCode class
        try:
            self.get_parser_tag_klass(tag_name=re_groups['start_name'])
        except Exception as e:
            raise ValidationError(e)

        if re_groups['start_name'] in parser.bbcodes.keys() \
                and not hasattr(parser.bbcodes[re_groups['start_name']], 'default_tag') \
                and not (
                    old_instance is not None and old_instance.tag_name == re_groups['start_name']):
            raise ValidationError(_('A BBCode tag with this name appears to already exist'))

        # Moreover, the used placeholders must be known by the BBCode parser and they must have the
        # same name, with some variations: eg {TEXT} can be used as {TEXT1} or {TEXT2} if two 'TEXT'
        # placeholders are needed
        placeholder_types = [
            re.findall(placeholder_content_re, placeholder) for placeholder in def_placeholders]
        placeholder_types = [
            placeholder_data[0][0] for placeholder_data in placeholder_types if placeholder_data]
        valid_placeholder_types = [
            placeholder for placeholder in placeholder_types
            if placeholder in parser.placeholders.keys()]

        if (not len(valid_placeholder_types) and not self.standalone) \
                or valid_placeholder_types != placeholder_types:
            raise ValidationError(
                _('You can only use placeholder names among: ' + str(parser.placeholders.keys()) +
                  '. If you need many placeholders of a specific type, you can append numbers to '
                  'them (eg. {TEXT1} or {TEXT2})'))

        super(BBCodeTag, self).clean()

    def save(self, *args, **kwargs):
        tag_re = bbcodde_standard_re if not self.standalone else bbcodde_standalone_re
        # Generate the tag name according to the tag definition
        re_groups = re.search(tag_re, self.tag_definition).groupdict()
        self.tag_name = re_groups['start_name']

        super(BBCodeTag, self).save(*args, **kwargs)
        # Ok, now the tag should be added to the BBCode parser for later use
        parser_tag_klass = self.parser_tag_klass
        parser = get_parser()
        parser.add_bbcode_tag(parser_tag_klass)

    def delete(self, *args, **kwargs):
        tag_name = self.tag_name
        super(BBCodeTag, self).delete(*args, **kwargs)

        # Remove the deleted tag from the BBCode parser pool of
        # available bbcode tags
        parser = get_parser()
        parser.bbcodes.pop(tag_name)

    def get_parser_tag_klass(self, tag_name=None):
        # Construct the inner Options class
        opts = self._meta
        tag_option_attrs = vars(BBCodeTagOptions)
        options_klass_attrs = {
            f.name: f.value_from_object(self) for f in opts.fields if f.name in tag_option_attrs}
        options_klass = type(force_str('Options'), (), options_klass_attrs)
        # Construct the outer BBCodeTag class
        tag_klass_attrs = {
            'name': self.tag_name if not tag_name else tag_name,
            'definition_string': self.tag_definition,
            'format_string': self.html_replacement,
            'Options': options_klass,
        }
        tag_klass = type(
            force_str('{}Tag'.format(self.tag_name)), (ParserBBCodeTag, ), tag_klass_attrs)
        return tag_klass

    @property
    def parser_tag_klass(self):
        return self.get_parser_tag_klass()


@python_2_unicode_compatible
class SmileyTag(models.Model):
    code = SmileyCodeField(max_length=60, verbose_name=_('Smiley code'), unique=True)
    image = models.ImageField(
        verbose_name=_('Smiley icon'), upload_to=bbcode_settings.SMILIES_UPLOAD_TO)
    image_width = models.PositiveIntegerField(
        verbose_name=_('Smiley icon width'), null=True, blank=True)
    image_height = models.PositiveIntegerField(
        verbose_name=_('Smiley icon height'), null=True, blank=True)

    # For later use
    emotion = models.CharField(
        max_length=100, verbose_name=_('Related emotion'), null=True, blank=True)
    display_on_editor = models.BooleanField(verbose_name=_('Display on editor'), default=True)

    class Meta:
        verbose_name = _('Smiley')
        verbose_name_plural = _('Smilies')
        app_label = 'precise_bbcode'

    def __str__(self):
        return '{}'.format(self.code)

    def save(self, *args, **kwargs):
        super(SmileyTag, self).save(*args, **kwargs)
        # The smiley should be added to the BBCode parser for later use
        parser = get_parser()
        parser.add_smiley(self.code, self.html_code)

    @property
    def html_code(self):
        """
        Returns the HTML associated with the current smiley tag object.
        """
        width = self.image_width or 'auto'
        height = self.image_height or 'auto'
        emotion = self.emotion or ''
        img = '<img src="{}" width="{}" height="{}" alt="{}" />'.format(
            self.image.url, width, height, emotion)
        return img
