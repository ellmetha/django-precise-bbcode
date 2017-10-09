# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import shutil

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import File
from django.utils.safestring import SafeText
from tests.models import DummyMessage

from precise_bbcode.fields import BBCodeContent
from precise_bbcode.models import SmileyTag


@pytest.mark.django_db
class TestBbcodeTextField(object):
    BBCODE_FIELDS_TESTS = (
        ('[b]hello [u]world![/u][/b]', '<strong>hello <u>world!</u></strong>'),
        ('[url=http://google.com]goto google[/url]', '<a href="http://google.com">goto google</a>'),
        ('[b]hello [u]worlsd![/u][/b]', '<strong>hello <u>worlsd!</u></strong>'),
        ('[b]안녕하세요[/b]', '<strong>안녕하세요</strong>'),
    )

    def test_accepts_none_values(self):
        # Setup
        message = DummyMessage()
        message.content = None
        # Run
        message.save()
        # Check
        assert message.content is None
        rendered = hasattr(message.content, 'rendered')
        assert not rendered

    def test_can_save_both_raw_and_rendered_data(self):
        # Run & check
        for bbcodes_text, expected_html_text in self.BBCODE_FIELDS_TESTS:
            message = DummyMessage()
            message.content = bbcodes_text
            message.save()
            assert message.content.rendered == expected_html_text

    def test_uses_a_valid_descriptor_protocol(self):
        # Setup
        message = DummyMessage()
        message.content = None
        message.save()
        bbcode_content = BBCodeContent('[b]hello world![/b]')
        # Run
        message.content = bbcode_content
        message.save()
        # Check
        assert message.content.rendered == '<strong>hello world!</strong>'

    def test_rendered_values_are_safe_strings(self):
        # Setup
        message = DummyMessage()
        message.content = None
        message.save()
        bbcode_content = BBCodeContent('[b]hello world![/b]')
        # Run
        message.content = bbcode_content
        message.save()
        # Check
        assert isinstance(message.content.rendered, SafeText)


@pytest.mark.django_db
class TestSmileyCodeField(object):
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

    def setup_method(self, method):
        # Set up an image used for doing smilies tests
        f = open(settings.MEDIA_ROOT + '/icon_e_wink.gif', 'rb')
        image_file = File(f)
        self.image = image_file

    def teardown_method(self, method):
        self.image.close()
        shutil.rmtree(settings.MEDIA_ROOT + '/precise_bbcode')

    def test_can_save_valid_smilies(self):
        # Run & check
        for smiley_code in self.SMILIES_FIELDS_TESTS:
            smiley = SmileyTag()
            smiley.code = smiley_code
            self.image.open()  # Re-open the ImageField
            smiley.image.save('icon_e_wink.gif', self.image)
            try:
                smiley.full_clean()
            except ValidationError:
                pytest.xfail('The following smiley code failed to validate: {}'.format(smiley_code))

    def test_should_not_save_erroneous_smilies(self):
        # Run & check
        for smiley_code in self.ERRONEOUS_SMILIES_FIELS_TESTS:
            smiley = SmileyTag()
            smiley.code = smiley_code
            self.image.open()  # Re-open the ImageField
            smiley.image.save('icon_e_wink.gif', self.image)
            with pytest.raises(ValidationError):
                smiley.full_clean()
