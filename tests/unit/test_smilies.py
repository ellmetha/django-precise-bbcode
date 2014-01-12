# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals

# Third party imports
from django.conf import settings
from django.core.files import File
from django.test import TestCase

# Local application / specific library imports
from precise_bbcode.models import SmileyTag
from precise_bbcode.parser import get_parser


class TestSmiley(TestCase):
    SMILIES_TESTS = (
        (':test:', '<img src="precise_bbcode/smilies/icon_e_wink.gif" width="auto" height="auto" alt="" />'),
        ('[list][*]:test: hello\n[/list]', '<ul><li><img src="precise_bbcode/smilies/icon_e_wink.gif" width="auto" height="auto" alt="" /> hello</li></ul>'),
        ('[quote]hello :test:[/quote]', '<blockquote>hello <img src="precise_bbcode/smilies/icon_e_wink.gif" width="auto" height="auto" alt="" /></blockquote>'),
        ('[code]hello :test:[/code]', '<code>hello :test:</code>'),
    )

    def setUp(self):
        self.parser = get_parser()
        # Set up an image used for doing smilies tests
        f = open(settings.MEDIA_ROOT + "/icon_e_wink.gif", "rb")
        image_file = File(f)
        self.image = image_file
        # Set up a smiley tag
        smiley = SmileyTag()
        smiley.code = ':test:'
        smiley.image.save('icon_e_wink.gif', self.image)
        smiley.save()

    def tearDown(self):
        self.image.close()
        smilies = SmileyTag.objects.all()
        for smiley in smilies:
            try:
                smiley.image.delete()
            except:
                pass

    def test_can_render_valid_smilies(self):
        # Run & check
        for bbcodes_text, expected_html_text in self.SMILIES_TESTS:
            result = self.parser.render(bbcodes_text)
            self.assertEqual(result, expected_html_text)
