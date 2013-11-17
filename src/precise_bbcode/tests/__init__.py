# -*- coding: utf-8 -*-

# Standard library imports
import pkgutil
import unittest

# Third party imports
from django.db import models

# Local application / specific library imports
from precise_bbcode.fields import BBCodeBlobField
from precise_bbcode.fields import BBCodeTextField


class TestMessage(models.Model):
    """
    This model will be use for testing purposes.
    """
    content = BBCodeTextField(null=True, blank=True)
    blob_content = BBCodeBlobField(null=True, blank=True)


# Sub-packages imports
from fields import *
from parser import *
from tags import *
from templatetags import *
