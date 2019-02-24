from django.db import models

from precise_bbcode.fields import BBCodeTextField


class DummyMessage(models.Model):
    """
    This model will be use for testing purposes.
    """
    content = BBCodeTextField(null=True, blank=True)

    class Meta:
        app_label = 'tests'
