# -*- coding: utf-8 -*-

# Standard library imports
import pkgutil
import unittest

# Third party imports
from django.db import models

# Local application / specific library imports
from precise_bbcode.fields import BBCodeTextField


class TestMessage(models.Model):
    """
    This model will be use for testing purposes.
    """
    content = BBCodeTextField(null=True, blank=True)


# Sub-packages imports
from .test_fields import *
from .test_parser import *
from .test_tags import *
from .test_templatetags import *
