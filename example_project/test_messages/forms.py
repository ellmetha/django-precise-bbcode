from django import forms

from .models import TestMessage


class TestMessageForm(forms.ModelForm):
    class Meta:
        model = TestMessage
        fields = ['bbcode_content', ]

    def __init__(self, *args, **kwargs):
        super(TestMessageForm, self).__init__(*args, **kwargs)
        self.fields['bbcode_content'].widget.attrs['class'] = 'form-control textarea'
