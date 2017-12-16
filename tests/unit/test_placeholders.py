# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re

import pytest
from django.core.exceptions import ImproperlyConfigured

from precise_bbcode.bbcode import BBCodeParserLoader
from precise_bbcode.bbcode import get_parser
from precise_bbcode.bbcode.defaults.placeholder import _color_re
from precise_bbcode.bbcode.defaults.placeholder import _email_re
from precise_bbcode.bbcode.defaults.placeholder import _number_re
from precise_bbcode.bbcode.defaults.placeholder import _simpletext_re
from precise_bbcode.bbcode.defaults.placeholder import _text_re
from precise_bbcode.bbcode.exceptions import InvalidBBCodePlaholder
from precise_bbcode.bbcode.placeholder import BBCodePlaceholder
from precise_bbcode.bbcode.regexes import url_re
from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.placeholder_pool import PlaceholderAlreadyRegistered
from precise_bbcode.placeholder_pool import PlaceholderNotRegistered
from precise_bbcode.placeholder_pool import placeholder_pool
from precise_bbcode.tag_pool import tag_pool


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


class FooPlaceholder(BBCodePlaceholder):
    name = 'foo'
    pattern = re.compile(r'^[\d]*$')


class DummyPlaceholder(BBCodePlaceholder):
    name = 'dummy'
    pattern = re.compile(r'^[\w]*$')


class FooBBCodeTag(BBCodeTag):
    name = 'xyz'
    definition_string = '[xyz]{FOO}[/xyz]'
    format_string = '<span class="foo">{FOO}</span>'


class DummyBBCodeTag(BBCodeTag):
    name = 'dummy'
    definition_string = '[dummy]{DUMMY}[/dummy]'
    format_string = '<span class="dummy">{DUMMY}</span'


@pytest.mark.django_db
class TestPlaceholderPool(object):
    TAGS_TESTS = (
        ('[xyz]hello world![/xyz]', '[xyz]hello world![/xyz]'),
        ('[xyz]12[/xyz]', '<span class="foo">12</span>'),
    )

    def setup_method(self, method):
        self.parser = get_parser()

    def test_should_raise_if_a_placeholder_is_registered_twice(self):
        # Setup
        number_of_placeholders_before = len(placeholder_pool.get_placeholders())
        placeholder_pool.register_placeholder(FooPlaceholder)
        # Run & check
        # Let's add it a second time. We should catch an exception
        with pytest.raises(PlaceholderAlreadyRegistered):
            placeholder_pool.register_placeholder(FooPlaceholder)
        # Let's make sure we have the same number of tags as before
        placeholder_pool.unregister_placeholder(FooPlaceholder)
        number_of_placeholders_after = len(placeholder_pool.get_placeholders())
        assert number_of_placeholders_before == number_of_placeholders_after

    def test_cannot_register_placeholders_with_incorrect_parent_classes(self):
        # Setup
        number_of_placeholders_before = len(placeholder_pool.get_placeholders())
        # Run & check
        with pytest.raises(ImproperlyConfigured):
            class ErrnoneousPlaceholder:
                pass
            placeholder_pool.register_placeholder(ErrnoneousPlaceholder)
        number_of_placeholders_after = len(placeholder_pool.get_placeholders())
        assert number_of_placeholders_before == number_of_placeholders_after

    def test_cannot_unregister_a_non_registered_placeholder(self):
        # Setup
        number_of_placeholders_before = len(placeholder_pool.get_placeholders())
        # Run & check
        with pytest.raises(PlaceholderNotRegistered):
            placeholder_pool.unregister_placeholder(FooPlaceholder)
        number_of_placeholders_after = len(placeholder_pool.get_placeholders())
        assert number_of_placeholders_before == number_of_placeholders_after

    def test_placeholders_can_be_used_with_tags(self):
        # Setup
        parser_loader = BBCodeParserLoader(parser=self.parser)
        placeholder_pool.register_placeholder(FooPlaceholder)
        placeholder_pool.register_placeholder(DummyPlaceholder)
        tag_pool.register_tag(FooBBCodeTag)
        tag_pool.register_tag(DummyBBCodeTag)
        parser_loader.init_bbcode_placeholders()
        parser_loader.init_bbcode_tags()
        # Run & check
        for bbcodes_text, expected_html_text in self.TAGS_TESTS:
            result = self.parser.render(bbcodes_text)
            assert result == expected_html_text
        placeholder_pool.unregister_placeholder(FooPlaceholder)
        placeholder_pool.unregister_placeholder(DummyPlaceholder)


class TestPlaceholder(object):
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

    def setup_method(self, method):
        self.parser = get_parser()
        self.parser.add_bbcode_tag(SizeTag)
        self.parser.add_bbcode_tag(ErroredSizeTag)
        self.parser.add_bbcode_tag(DayTag)

    def test_regexes_provided_by_default_are_valid(self):
        # Run & check
        for _, re_tests in self.DEFAULT_PLACEHOLDERS_RE_TESTS.items():
            for test in re_tests['tests']:
                assert re.search(re_tests['re'], test) is not None

    def test_provided_by_default_are_valid(self):
        for bbcodes_text, expected_html_text in self.DEFAULT_PLACEHOLDERS_TESTS:
            result = self.parser.render(bbcodes_text)
            assert result == expected_html_text

    def test_provided_by_default_cannot_be_rendered_if_they_are_not_used_correctly(self):
        for bbcodes_text, expected_html_text in self.ERRORED_DEFAULT_PLACEHOLDERS_TESTS:
            result = self.parser.render(bbcodes_text)
            assert result == expected_html_text

    def test_that_are_invalid_should_raise_at_runtime(self):
        # Run & check
        with pytest.raises(InvalidBBCodePlaholder):
            class InvalidePlaceholder1(BBCodePlaceholder):
                pass
        with pytest.raises(InvalidBBCodePlaholder):
            class InvalidePlaceholder2(BBCodePlaceholder):
                delattr(BBCodePlaceholder, 'name')
        with pytest.raises(InvalidBBCodePlaholder):
            class InvalidePlaceholder3(BBCodePlaceholder):
                name = 'bad placeholder name'
        with pytest.raises(InvalidBBCodePlaholder):
            class InvalidePlaceholder4(BBCodePlaceholder):
                name = 'correctname'
                pattern = 'incorrect pattern'
