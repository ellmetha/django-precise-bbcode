# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals

# Third party imports
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.test import TestCase

# Local application / specific library imports
from precise_bbcode.models import BBCodeTag
from precise_bbcode.parser import get_parser
from precise_bbcode.parser import _init_bbcode_tags
from precise_bbcode.parser import _init_custom_bbcode_tags
from precise_bbcode.tag_base import TagBase
from precise_bbcode.tag_pool import TagAlreadyRegistered
from precise_bbcode.tag_pool import TagNotRegistered
from precise_bbcode.tag_pool import tag_pool


class FooTag(TagBase):
    tag_name = "foo"
    render_embedded = False

    def render(self, name, value, option=None, parent=None):
        return '<pre>{}</pre>'.format(value)


class FooTagSub(FooTag):
    tag_name = "foo2"
    render_embedded = False


class BarTag(TagBase):
    tag_name = "bar"

    def render(self, name, value, option=None, parent=None):
        if not option:
            return '<div class="bar">{}</div>'.format(value)
        return '<div class="bar" style="color:{};">{}</div>'.format(option, value)


class TagsTestCase(TestCase):
    TAGS_TESTS = (
        ('[foo]hello world![/foo]', '<pre>hello world!</pre>'),
        ('[bar]hello world![/bar]', '<div class="bar">hello world!</div>'),
        ('[foo]hello [bar]world![/bar][/foo]', '<pre>hello [bar]world![/bar]</pre>'),
        ('[bar]hello [foo]world![/foo][/bar]', '<div class="bar">hello <pre>world!</pre></div>'),
        ('[bar]안녕하세요![/bar]', '<div class="bar">안녕하세요!</div>'),
    )

    def setUp(self):
        self.parser = get_parser()

    def test_register_tag_twice_should_raise(self):
        # Setup
        number_of_tags_before = len(tag_pool.get_tags())
        tag_pool.register_tag(FooTag)
        # Run & check
        # Let's add it a second time. We should catch an exception
        with self.assertRaises(TagAlreadyRegistered):
            tag_pool.register_tag(FooTag)
        # Let's make sure we have the same number of tags as before
        tag_pool.unregister_tag(FooTag)
        number_of_tags_after = len(tag_pool.get_tags())
        self.assertEqual(number_of_tags_before, number_of_tags_after)

    def test_erroneous_tag_definition_should_raise(self):
        # Setup
        number_of_tags_before = len(tag_pool.get_tags())
        # Run & check
        with self.assertRaises(ImproperlyConfigured):
            class ErrnoneousTag1(TagBase):
                pass
        with self.assertRaises(ImproperlyConfigured):
            class ErrnoneousTag2(TagBase):
                delattr(TagBase, 'tag_name')
        with self.assertRaises(ValueError):
            class ErrnoneousTag3(TagBase):
                tag_name = "it's a bad tag name"
        number_of_tags_after = len(tag_pool.get_tags())
        self.assertEqual(number_of_tags_before, number_of_tags_after)

    def test_register_invalid_tag_should_raise(self):
        # Setup
        number_of_tags_before = len(tag_pool.get_tags())
        # Run & check
        with self.assertRaises(ImproperlyConfigured):
            class ErrnoneousTag4:
                pass
            tag_pool.register_tag(ErrnoneousTag4)
        number_of_tags_after = len(tag_pool.get_tags())
        self.assertEqual(number_of_tags_before, number_of_tags_after)

    def test_unregister_non_existing_tag_should_raise(self):
        # Setup
        number_of_tags_before = len(tag_pool.get_tags())
        # Run & check
        with self.assertRaises(TagNotRegistered):
            tag_pool.unregister_tag(FooTagSub)
        number_of_tags_after = len(tag_pool.get_tags())
        self.assertEqual(number_of_tags_before, number_of_tags_after)

    def test_render_tags(self):
        # Setup
        tag_pool.register_tag(FooTag)
        tag_pool.register_tag(BarTag)
        _init_bbcode_tags(self.parser)
        # Run & check
        for bbcodes_text, expected_html_text in self.TAGS_TESTS:
            result = self.parser.render(bbcodes_text)
            self.assertEqual(result, expected_html_text)


class CustomTagsTestCase(TestCase):
    ERRONEOUS_TAGS_TESTS = (
        {'tag_definition': '[tag]', 'html_replacement': ''},
        {'tag_definition': 'it\s not a tag', 'html_replacement': ''},
        {'tag_definition': '[first]{TEXT1}[/end]', 'html_replacement': '<p>{TEXT1}</p>'},
        {'tag_definition': '[t2y={TEXT1}]{TEXT1}[/t2y]', 'html_replacement': '<b>{TEXT1}</b>'},
        {'tag_definition': '[tag2]{TEXT1}[/tag2]', 'html_replacement': '<p>{TEXT1}</p>', 'standalone': True},
        {'tag_definition': '[start]{TEXT1}[/end]', 'html_replacement': '<p>{TEXT1}</p>'},
        {'tag_definition': '[start]{TEXT1}[/end]', 'html_replacement': '<p>{TEXT1}</p>'},
        {'tag_definition': '[start]{TEXT1}[/end]', 'html_replacement': '<p>{TEXT2}</p>'},
        {'tag_definition': '[start={TEXT1}]{TEXT1}[/end]', 'html_replacement': '<p style="color:{TEXT1};">{TEXT1}</p>'},
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
        {'tag_definition': '[foo]{TEXT1}[/foo ]', 'html_replacement': '<span>{TEXT}</span>'},
    )

    VALID_TAG_TESTS = (
        {'tag_definition': '[pre]{TEXT}[/pre]', 'html_replacement': '<pre>{TEXT}</pre>'},
        {'tag_definition': '[pre2={COLOR}]{TEXT1}[/pre2]', 'html_replacement': '<pre style="color:{COLOR};">{TEXT1}</pre>'},
        {'tag_definition': '[hrcustom]', 'html_replacement': '<hr />', 'standalone': True},
        {'tag_definition': '[h]{TEXT}[/h]', 'html_replacement': '<strong>{TEXT}</strong>', 'helpline': 'Display your text in bold'},
        {'tag_definition': '[hbold]{TEXT}[/hbold]', 'html_replacement': '<strong>{TEXT}</strong>', 'display_on_editor': False},
        {'tag_definition': '[pre3]{TEXT}[/pre3]', 'html_replacement': '<pre>{TEXT}</pre>', 'newline_closes': True},
        {'tag_definition': '[pre4]{TEXT}[/pre4]', 'html_replacement': '<pre>{TEXT}</pre>', 'same_tag_closes': True},
        {'tag_definition': '[troll]{TEXT}[/troll]', 'html_replacement': '<div class="troll">{TEXT}</div>', 'end_tag_closes': True},
        {'tag_definition': '[troll1]{TEXT}[/troll1]', 'html_replacement': '<div class="troll">{TEXT}</div>', 'transform_newlines': True},
        {'tag_definition': '[idea]{TEXT1}[/idea]', 'html_replacement': '<div class="idea">{TEXT1}</div>', 'render_embedded': False},
        {'tag_definition': '[idea1]{TEXT1}[/idea1]', 'html_replacement': '<div class="idea">{TEXT1}</div>', 'escape_html': False},
        {'tag_definition': '[link]{URL}[/link]', 'html_replacement': '<div class="idea">{URL}</div>', 'replace_links': False},
        {'tag_definition': '[link1]{URL}[/link1]', 'html_replacement': '<div class="idea">{URL}</div>', 'strip': True},
        {'tag_definition': '[mailto]{EMAIL}[/mailto]', 'html_replacement': '<a href="mailto:{EMAIL}">{EMAIL}</a>', 'swallow_trailing_newline': True},
    )

    def setUp(self):
        self.parser = get_parser()

    def test_erroneous_tags_cleaning(self):
        # Run & check
        for tag_dict in self.ERRONEOUS_TAGS_TESTS:
            with self.assertRaises(ValidationError):
                tag = BBCodeTag(**tag_dict)
                tag.clean()

    def test_valid_tags_cleaning(self):
        # Run & check
        for tag_dict in self.VALID_TAG_TESTS:
            tag = BBCodeTag(**tag_dict)
            try:
                tag.clean()
            except ValidationError as e:
                self.fail("The following BBCode failed to validate: {}".format(tag_dict))

    def test_parser_args_retrieval(self):
        # Setup
        tag = BBCodeTag(**{'tag_definition': '[io]{TEXT}[/io]', 'html_replacement': '<b>{TEXT}</b>'})
        tag.save()
        # Run & check
        self.assertEqual(tag.parser_args, (['io', '[io]{TEXT}[/io]', '<b>{TEXT}</b>'],
                         {'display_on_editor': True, 'end_tag_closes': False, 'escape_html': True,
                          'helpline': None, 'newline_closes': False, 'render_embedded': True,
                          'replace_links': True, 'same_tag_closes': False, 'standalone': False, 'strip': False,
                          'swallow_trailing_newline': False, 'transform_newlines': True}))

    def test_valid_tag_rendering(self):
        # Setup
        tag = BBCodeTag(**{'tag_definition': '[mail]{EMAIL}[/mail]',
                        'html_replacement': '<a href="mailto:{EMAIL}">{EMAIL}</a>', 'swallow_trailing_newline': True})
        tag.save()
        _init_custom_bbcode_tags(self.parser)
        # Run & check
        self.assertEqual(self.parser.render('[mail]xyz@xyz.com[/mail]'), '<a href="mailto:xyz@xyz.com">xyz@xyz.com</a>')
