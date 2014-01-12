# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals

# Third party imports
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import File
from django.test import TestCase

# Local application / specific library imports
from precise_bbcode.fields import BBCodeContent
from precise_bbcode.models import SmileyTag
from tests.models import TestMessage


class TestBbcodeTextField(TestCase):
    BBCODE_FIELDS_TESTS = (
        ('[b]hello [u]world![/u][/b]', '<strong>hello <u>world!</u></strong>'),
        ('[url=http://google.com]goto google[/url]', '<a href="http://google.com">goto google</a>'),
        ('[b]hello [u]worlsd![/u][/b]', '<strong>hello <u>worlsd!</u></strong>'),
        ('[b]안녕하세요[/b]', '<strong>안녕하세요</strong>'),
    )

    def test_accepts_none_values(self):
        # Setup
        message = TestMessage()
        message.content = None
        # Run
        message.save()
        # Check
        self.assertIsNone(message.content)
        rendered = hasattr(message.content, 'rendered')
        self.assertFalse(rendered)

    def test_can_save_both_raw_and_rendered_data(self):
        # Run & check
        for bbcodes_text, expected_html_text in self.BBCODE_FIELDS_TESTS:
            message = TestMessage()
            message.content = bbcodes_text
            message.save()
            self.assertEqual(message.content.rendered, expected_html_text)

    def test_uses_a_valid_descriptor_protocol(self):
        # Setup
        message = TestMessage()
        message.content = None
        message.save()
        bbcode_content = BBCodeContent('[b]hello world![/b]')
        # Run
        message.content = bbcode_content
        message.save()
        # Check
        self.assertEqual(message.content.rendered, '<strong>hello world!</strong>')


class TestSmileyCodeField(TestCase):
    SMILIES_FIELDS_TESTS = (
        ';-)',
        ':lol:',
        '>_<',
        '><',
        ':emotion:',
        '(-_-)',
        '(<_>)',
    )

    ERRONEOUS_SMILIES_FIELS_TESTS = (
        'text with some spaces',
        ':i\'m happy:',
    )

    def setUp(self):
        # Set up an image used for doing smilies tests
        f = open(settings.MEDIA_ROOT + "/icon_e_wink.gif", "rb")
        image_file = File(f)
        self.image = image_file

    def tearDown(self):
        self.image.close()
        smilies = SmileyTag.objects.all()
        for smiley in smilies:
            try:
                smiley.image.delete()
            except:
                pass

    def test_can_save_valid_smilies(self):
        # Run & check
        for smiley_code in self.SMILIES_FIELDS_TESTS:
            smiley = SmileyTag()
            smiley.code = smiley_code
            smiley.image.save('icon_e_wink.gif', self.image)
            try:
                smiley.full_clean()
            except ValidationError:
                self.fail("The following smiley code failed to validate: {}".format(smiley_code))

    def test_should_not_save_erroneous_smilies(self):
        # Run & check
        for smiley_code in self.ERRONEOUS_SMILIES_FIELS_TESTS:
            smiley = SmileyTag()
            smiley.code = smiley_code
            smiley.image.save('icon_e_wink.gif', self.image)
            with self.assertRaises(ValidationError):
                smiley.full_clean()
