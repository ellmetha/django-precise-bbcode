# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import TestMessageForm
from .models import TestMessage


class TestMessageCreate(CreateView):
    model = TestMessage
    form_class = TestMessageForm
    template_name = 'test_messages/create_bbcode_message.html'

    def get_success_url(self):
        return "{0}?success=true".format(
            reverse_lazy('bbcode-message-detail', kwargs={'message_pk': self.object.id})
        )


class TestMessageDetailView(DetailView):
    model = TestMessage
    template_name = 'test_messages/bbcode_message.html'
    pk_url_kwarg = 'message_pk'
