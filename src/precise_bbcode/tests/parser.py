# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.test import TestCase

# Local application / specific library imports
from precise_bbcode.parser import BBCodeParser


class ParserTestCase(TestCase):
    RENDERING_TESTS = (
        # BBcodes without errors
        ('[b]hello world![/b]', '<strong>hello world!</strong>'),
        # BBCodes with syntactics errors
        ('[b]z sdf s s', '[b]z sdf s s'),
    )

    def setUp(self):
        self.parser = BBCodeParser()

    def test_rendering(self):
        for bbcodes_text, expected_html_text in self.RENDERING_TESTS:
            result = self.parser.render(bbcodes_text)
            self.assertEqual(result, expected_html_text)
