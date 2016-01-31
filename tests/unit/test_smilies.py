# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import shutil

from django.conf import settings
from django.core.files import File
import pytest

from precise_bbcode.bbcode import BBCodeParserLoader
from precise_bbcode.bbcode import get_parser
from precise_bbcode.models import SmileyTag


@pytest.mark.django_db
class TestSmiley(object):
    SMILIES_TESTS = (
        (':test:', '<img src="precise_bbcode/smilies/icon_e_wink.gif" width="auto" height="auto" alt="" />'),
        ('[list][*]:test: hello\n[/list]', '<ul><li><img src="precise_bbcode/smilies/icon_e_wink.gif" width="auto" height="auto" alt="" /> hello</li></ul>'),
        ('[quote]hello :test:[/quote]', '<blockquote>hello <img src="precise_bbcode/smilies/icon_e_wink.gif" width="auto" height="auto" alt="" /></blockquote>'),
        ('[code]hello :test:[/code]', '<code>hello :test:</code>'),
    )

    def create_smilies(self):
        self.parser = get_parser()
        self.parser_loader = BBCodeParserLoader(parser=self.parser)
        # Set up an image used for doing smilies tests
        f = open(settings.MEDIA_ROOT + '/icon_e_wink.gif', 'rb')
        image_file = File(f)
        self.image = image_file
        # Set up a smiley tag
        smiley = SmileyTag()
        smiley.code = ':test:'
        smiley.image.save('icon_e_wink.gif', self.image)
        smiley.save()
        self.parser_loader.init_bbcode_smilies()

    def teardown_method(self, method):
        self.image.close()
        shutil.rmtree(settings.MEDIA_ROOT + '/precise_bbcode')

    def test_can_render_valid_smilies(self):
        # Setup
        self.create_smilies()
        # Run & check
        for bbcodes_text, expected_html_text in self.SMILIES_TESTS:
            result = self.parser.render(bbcodes_text)
            assert result == expected_html_text
