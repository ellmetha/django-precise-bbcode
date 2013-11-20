# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import ugettext as _

# Local application / specific library imports
from .models import TestMessage


class TestMessageForm(forms.ModelForm):
    class Meta:
        model = TestMessage
        fields = ['bbcode_content', ]

    def __init__(self, *args, **kwargs):
        super(TestMessageForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.layout = Layout('bbcode_content')
        self.helper.add_input(Submit('submit', _('Submit')))
