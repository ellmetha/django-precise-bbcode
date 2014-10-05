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

    def setUp(self):
        self.parser = get_parser()

    def test_regex_provided_by_default_are_valid(self):
        # Run & check
        for _, re_tests in self.DEFAULT_PLACEHOLDERS_RE_TESTS.items():
            for test in re_tests['tests']:
                self.assertIsNotNone(re.search(re_tests['re'], test))
