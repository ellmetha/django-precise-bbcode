# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.db import models

# Local application / specific library imports
from precise_bbcode.fields import BBCodeTextField


class TestMessage(models.Model):
    """
    This model will be use for testing purposes.
    """
    content = BBCodeTextField(null=True, blank=True)
