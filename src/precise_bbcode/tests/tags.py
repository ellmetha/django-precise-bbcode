# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.core.exceptions import ValidationError
from django.test import TestCase

# Local application / specific library imports
from precise_bbcode.models import BBCodeTag
from precise_bbcode.parser import get_parser


class CustomTagsTestCase(TestCase):
    ERRONEOUS_TAGS_TESTS = (
        {'tag_definition': '[tag]', 'html_replacement': ''},
        {'tag_definition': 'it\s not a tag', 'html_replacement': ''},
        {'tag_definition': '[tag2]{TEXT1}[/tag2]', 'html_replacement': '<p>{TEXT1}</p>', 'standalone': True},
        {'tag_definition': '[start]{TEXT1}[/end]', 'html_replacement': '<p>{TEXT1}</p>'},
        {'tag_definition': '[start]{TEXT1}[/end]', 'html_replacement': '<p>{TEXT1}</p>'},
        {'tag_definition': '[b]{TEXT1}[/b]', 'html_replacement': '<b>{TEXT1}</b>'},
        {'tag_definition': '[justify]{TEXT1}[/justify]', 'html_replacement': '<div style="text-align:justify;"></div>'},
        {'tag_definition': '[center][/center]', 'html_replacement': '<div style="text-align:center;">{TEXT1}</div>'},
        {'tag_definition': '[spe={COLOR}]{TEXT}[/spe]', 'html_replacement': '<div class="spe">{TEXT}</div>'},
        {'tag_definition': '[spe]{TEXT}[/spe]', 'html_replacement': '<div class="spe" style="color:{COLOR};">{TEXT}</div>'},
        {'tag_definition': '[spe]{UNKNOWN}[/spe]', 'html_replacement': '<div>{UNKNOWN}</div>'},
        {'tag_definition': '[io]{TEXT#1}[/io]', 'html_replacement': '<span>{TEXT#1}</span>'},
        {'tag_definition': '[io]{TEXTa}[/io]', 'html_replacement': '<span>{TEXTb}</span>'},
        {'tag_definition': '[ test]{TEXT1}[/test]', 'html_replacement': '<span>{TEXT}</span>'},
        {'tag_definition': '[test ]{TEXT1}[/test]', 'html_replacement': '<span>{TEXT}</span>'},
        {'tag_definition': '[test]{TEXT1}[/ test ]', 'html_replacement': '<span>{TEXT}</span>'},
        {'tag_definition': '[test]{TEXT1}[/test ]', 'html_replacement': '<span>{TEXT}</span>'},
    )

    def setUp(self):
        self.parser = get_parser()

    def test_erroneous_tags_saving(self):
        # Run & check
        for tag_dict in self.ERRONEOUS_TAGS_TESTS:
            with self.assertRaises(ValidationError):
                tag = BBCodeTag(**tag_dict)
                tag.clean()
