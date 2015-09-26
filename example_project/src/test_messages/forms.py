# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

from .models import TestMessage


class TestMessageForm(forms.ModelForm):
    class Meta:
        model = TestMessage
        fields = ['bbcode_content', ]
