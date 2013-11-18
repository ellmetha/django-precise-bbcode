# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from precise_bbcode.fields import BBCodeTextField

# Local application / specific library imports


class TestMessage(models.Model):
    bbcode_content = BBCodeTextField(verbose_name=_('BBCode content'))

    class Meta:
        verbose_name = _('Test message')
        verbose_name_plural = _('Test messages')
        app_label = 'test_messages'

    def __unicode__(self):
        return u'{}'.format(self.id if self.id else _('new message'))
