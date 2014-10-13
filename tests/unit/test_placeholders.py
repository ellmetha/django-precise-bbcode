# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import re

# Third party imports
from django.test import TestCase

# Local application / specific library imports
from precise_bbcode import get_parser
from precise_bbcode.bbcode.defaults.placeholder import _color_re
from precise_bbcode.bbcode.defaults.placeholder import _email_re
from precise_bbcode.bbcode.defaults.placeholder import _number_re
from precise_bbcode.bbcode.defaults.placeholder import _simpletext_re
from precise_bbcode.bbcode.defaults.placeholder import _text_re
from precise_bbcode.bbcode.defaults.placeholder import url_re
from precise_bbcode.bbcode.exceptions import InvalidBBCodePlaholder
from precise_bbcode.bbcode.placeholder import BBCodePlaceholder
from precise_bbcode.bbcode.tag import BBCodeTag


class SizeTag(BBCodeTag):
    name = 'siz'
    definition_string = '[siz={RANGE=4,7}]{TEXT}[/siz]'
    format_string = '<span style="font-size:{RANGE=4,7}px;">{TEXT}</span>'


class ErroredSizeTag(BBCodeTag):
    name = 's2'
    definition_string = '[s2={RANGE=a,7}]{TEXT}[/s2]'
    format_string = '<span style="font-size:{RANGE=a,7}px;">{TEXT}</span>'


class DayTag(BBCodeTag):
    name = 'day'
    definition_string = '[day]{CHOICE=monday,tuesday,wednesday,tuesday,friday,saturday,sunday}[/day]'
    format_string = '<h5>{CHOICE=monday,tuesday,wednesday,tuesday,friday,saturday,sunday}</h5>'


class TestPlaceholder(TestCase):
    DEFAULT_PLACEHOLDERS_RE_TESTS = {
        'text': {
            're': _text_re,
            'tests': (
                'hello world',
                'hello\nworld',
                '   hello world     ',
                'http://asdf.xxxx.yyyy.com/vvvvv/PublicPages/Login.aspx?ReturnUrl=%2fvvvvv%2f(asdf@qwertybean.com/qwertybean)',
                '12902',
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer pretium, mi ac molestie ornare, urna sem fermentum erat, malesuada interdum sapien turpis sit amet eros.\nPhasellus quis mi velit. Cras porttitor dui faucibus rhoncus fringilla. Cras non fringilla est. \nCurabitur sollicitudin nisi quis sem sodales, quis blandit massa rhoncus. Nam porta at lacus semper gravida.\n',
                '안녕하세요!',
            )
        },
        'simpletext': {
            're': _simpletext_re,
            'tests': (
                'hello world',
                'slugify-u-21'
                'hello91',
            )
        },
        'url': {
            're': url_re,
            'tests': (
                'http://foo.com/blah_blah',
                '(Something like http://foo.com/blah_blah)',
                'http://foo.com/blah_blah_(wikipedia)',
                'http://foo.com/more_(than)_one_(parens)',
                '(Something like http://foo.com/blah_blah_(wikipedia))',
                'http://foo.com/blah_(wikipedia)#cite-1',
                'http://foo.com/blah_(wikipedia)_blah#cite-1',
                'http://foo.com/(something)?after=parens',
                'http://foo.com/blah_blah.',
                'http://foo.com/blah_blah/.',
                '<http://foo.com/blah_blah>',
                '<http://foo.com/blah_blah/>',
                'http://foo.com/blah_blah,',
                'http://www.extinguishedscholar.com/wpglob/?p=364.',
                '<tag>http://example.com</tag>',
                'Just a www.example.com link.',
                'http://example.com/something?with,commas,in,url, but not at end',
                'bit.ly/foo',
                'http://asdf.xxxx.yyyy.com/vvvvv/PublicPages/Login.aspx?ReturnUrl=%2fvvvvv%2f(asdf@qwertybean.com/qwertybean)',
                'http://something.xx:8080'
            )
        },
        'email': {
            're': _email_re,
            'tests': (
                'president@whitehouse.gov',
                'xyz.xyz@xy.com',
                'hello_world@rt.rt',
                '"email"@domain.com',
                'a@b.cc',
                'joe@aol.com',
                'joe@wrox.co.uk',
                'joe@domain.info',
                'asmith@mactec.com',
                'foo12@foo.edu ',
                'bob.smith@foo.tv',
                'bob-smith@foo.com',
                'bob.smith@foo.com',
                'bob_smith@foo.com',
                'bob@somewhere.com',
                'bob.jones@[1.1.1.1]',
                'bob@a.b.c.d.info',
                '&lt;ab@cd.ef&gt;',
                'bob A. jones &lt;ab@cd.ef&gt;',
                'bob A. jones &lt;ab@[1.1.1.111]&gt;',
                'blah@127.0.0.1',
                'whatever@somewhere.museum',
                'foreignchars@myforeigncharsdomain.nu',
                'me+mysomething@mydomain.com',
                'u-s_e.r1@s-ub2.domain-name.museum:8080',
            )
        },
        'color': {
            're': _color_re,
            'tests': (
                'red',
                'blue',
                'pink',
                '#FFFFFF',
                '#fff000',
                '#FFF',
                '#3089a2',
            )
        },
        'number': {
            're': _number_re,
            'tests': (
                '12',
                '1289101',
                '-121',
                '89.12',
                '100000000000001',
                '10000000000000,1',
                '-12,1990000000000000001',
            )
        }
    }

    DEFAULT_PLACEHOLDERS_TESTS = (
        ('[siz=4]hello world![/siz]', '<span style="font-size:4px;">hello world!</span>'),
        ('[siz=5]hello world![/siz]', '<span style="font-size:5px;">hello world!</span>'),
        ('[siz=6]hello world![/siz]', '<span style="font-size:6px;">hello world!</span>'),
        ('[siz=7]hello world![/siz]', '<span style="font-size:7px;">hello world!</span>'),
        ('[siz=3]hello world![/siz]', '[siz=3]hello world![/siz]'),
        ('[siz=8]hello world![/siz]', '[siz=8]hello world![/siz]'),
        ('[siz=test]hello world![/siz]', '[siz=test]hello world![/siz]'),
        ('[day]tuesday[/day]', '<h5>tuesday</h5>'),
        ('[day]monday[/day]', '<h5>monday</h5>'),
        ('[day]sunday[/day]', '<h5>sunday</h5>'),
        ('[day]sun[/day]', '[day]sun[/day]'),
        ('[day]test, test[/day]', '[day]test, test[/day]'),
    )

    ERRORED_DEFAULT_PLACEHOLDERS_TESTS = (
        ('[s2=4]hello world![/s2]', '[s2=4]hello world![/s2]'),
    )

    def setUp(self):
        self.parser = get_parser()
        self.parser.add_bbcode_tag(SizeTag)
        self.parser.add_bbcode_tag(ErroredSizeTag)
        self.parser.add_bbcode_tag(DayTag)

    def test_regexes_provided_by_default_are_valid(self):
        # Run & check
        for _, re_tests in self.DEFAULT_PLACEHOLDERS_RE_TESTS.items():
            for test in re_tests['tests']:
                self.assertIsNotNone(re.search(re_tests['re'], test))

    def test_provided_by_default_are_valid(self):
        for bbcodes_text, expected_html_text in self.DEFAULT_PLACEHOLDERS_TESTS:
            result = self.parser.render(bbcodes_text)
            self.assertEqual(result, expected_html_text)

    def test_provided_by_default_cannot_be_rendered_if_they_are_not_used_correctly(self):
        for bbcodes_text, expected_html_text in self.ERRORED_DEFAULT_PLACEHOLDERS_TESTS:
            result = self.parser.render(bbcodes_text)
            self.assertEqual(result, expected_html_text)

    def test_that_are_invalid_should_raise_at_runtime(self):
        # Run & check
        with self.assertRaises(InvalidBBCodePlaholder):
            class InvalidePlaceholder1(BBCodePlaceholder):
                pass
        with self.assertRaises(InvalidBBCodePlaholder):
            class InvalidePlaceholder2(BBCodePlaceholder):
                delattr(BBCodePlaceholder, 'name')
        with self.assertRaises(InvalidBBCodePlaholder):
            class InvalidePlaceholder3(BBCodePlaceholder):
                name = 'bad placeholder name'
        with self.assertRaises(InvalidBBCodePlaholder):
            class InvalidePlaceholder4(BBCodePlaceholder):
                name = 'correctname'
                pattern = 'incorrect pattern'
