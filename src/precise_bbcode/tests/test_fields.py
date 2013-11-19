# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals

# Third party imports
from django.test import TestCase

# Local application / specific library imports
from precise_bbcode.tests import TestMessage


class FieldsTestCase(TestCase):
    BBCODE_FIELDS_TESTS = (
        ('[b]hello [u]world![/u][/b]', '<strong>hello <u>world!</u></strong>'),
        ('[url=http://google.com]goto google[/url]', '<a href="http://google.com">goto google</a>'),
        ('[b]hello [u]worlsd![/u][/b]', '<strong>hello <u>worlsd!</u></strong>'),
        ('[b]안녕하세요[/b]', '<strong>안녕하세요</strong>'),
    )

    def test_bbcode_text_field_accept_none_values(self):
        # Setup
        message = TestMessage()
        message.content = None
        # Run
        message.save()
        # Check
        self.assertIsNone(message.content)
        rendered = hasattr(message.content, 'rendered')
        self.assertFalse(rendered)

    def test_bbcode_text_field_saving(self):
        # Run & check
        for bbcodes_text, expected_html_text in self.BBCODE_FIELDS_TESTS:
            message = TestMessage()
            message.content = bbcodes_text
            message.save()
            self.assertEqual(message.content.rendered, expected_html_text)
