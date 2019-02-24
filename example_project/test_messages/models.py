from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from precise_bbcode.fields import BBCodeTextField


@python_2_unicode_compatible
class TestMessage(models.Model):
    bbcode_content = BBCodeTextField(verbose_name=_('BBCode content'))

    class Meta:
        verbose_name = _('Test message')
        verbose_name_plural = _('Test messages')
        app_label = 'test_messages'

    def __str__(self):
        return '{}'.format(self.id if self.id else _('new message'))
