# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from precise_bbcode.fields import BBCodeTextField


class TestMessage(models.Model):
    """
    This model will be use for testing purposes.
    """
    content = BBCodeTextField(null=True, blank=True)
