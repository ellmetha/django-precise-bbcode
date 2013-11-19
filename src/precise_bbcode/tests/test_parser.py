# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import re

# Third party imports
from django.test import TestCase

# Local application / specific library imports
from precise_bbcode.parser import get_parser
from precise_bbcode.parser import _color_re
from precise_bbcode.parser import _email_re
from precise_bbcode.parser import _number_re
from precise_bbcode.parser import _simpletext_re
from precise_bbcode.parser import _text_re
from precise_bbcode.parser import _url_re


class ParserTestCase(TestCase):
    DEFAULT_TAGS_RENDERING_TESTS = (
        # BBcodes without errors
        ('[b]hello world![/b]', '<strong>hello world!</strong>'),
        ('[b]hello [i]world![/i][/b]', '<strong>hello <em>world!</em></strong>'),
        ('[b]hello [ world![/b]', '<strong>hello [ world!</strong>'),
        ('[b]]he[llo [ w]orld![/b]', '<strong>]he[llo [ w]orld!</strong>'),
        ('[ b ]hello [u]world![/u][ /b ]', '<strong>hello <u>world!</u></strong>'),
        ('[b]hello [] world![/b]', '<strong>hello [] world!</strong>'),
        ('[list]\n[*]one\n[*]two\n[/list]', '<ul><li>one</li><li>two</li></ul>'),
        ('[list=1]\n[*]item 1\n[*]item 2\n[/list]', '<ol style="list-style-type:decimal;"><li>item 1</li><li>item 2</li></ol>'),
        ('[list] [*]Item 1 [*]Item 2 [*]Item 3   [/list]', '<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>'),
        ('>> some special chars >< <>', '&gt;&gt; some special chars &gt;&lt; &lt;&gt;'),
        ('"quoted text"', '&quot;quoted text&quot;'),
        ('>> some other special chars', '&gt;&gt; some other special chars'),
        ('[url]http://foo.com/bar.php?some--data[/url]', '<a href="http://foo.com/bar.php?some--data">http://foo.com/bar.php?some--data</a>'),
        ('[url]http://www.google.com[/url]', '<a href="http://www.google.com">http://www.google.com</a>'),
        ('[url=google.com]goto google[/url]', '<a href="http://google.com">goto google</a>'),
        ('[url=http://google.com][/url]', '<a href="http://google.com">http://google.com</a>'),
        ('[URL=google.com]goto google[/URL]', '<a href="http://google.com">goto google</a>'),
        ('[url=<script>alert(1);</script>]xss[/url]', '<a href="&lt;script&gt;alert(1);&lt;/script&gt;">xss</a>'),
        ('www.google.com foo.com/bar http://xyz.ci', '<a href="http://www.google.com">www.google.com</a> <a href="http://foo.com/bar">foo.com/bar</a> <a href="http://xyz.ci">http://xyz.ci</a>'),
        ('[url=relative/foo/bar.html]link[/url]', '<a href="relative/foo/bar.html">link</a>'),
        ('[url=/absolute/foo/bar.html]link[/url]', '<a href="/absolute/foo/bar.html">link</a>'),
        ('[url=./hello.html]world![/url]', '<a href="./hello.html">world!</a>'),
        ('[img]http://www.foo.com/bar/img.png[/img]', '<img src="http://www.foo.com/bar/img.png" alt="" />'),
        ('[quote] \r\nhello\nworld! [/quote]', '<blockquote>hello<br />world!</blockquote>'),
        ('[code][b]hello world![/b][/code]', '<code>[b]hello world![/b]</code>'),
        ('[color=green]goto [url=google.com]google website[/url][/color]', '<span style="color:green;">goto <a href="http://google.com">google website</a></span>'),
        ('[color=#FFFFFF]white[/color]', '<span style="color:#FFFFFF;">white</span>'),
        ('[color=<script></script>]xss[/color]', '[color=&lt;script&gt;&lt;/script&gt;]xss[/color]'),
        ('[COLOR=blue]hello world![/color]', '<span style="color:blue;">hello world!</span>'),
        # BBCodes with syntactic errors
        ('[b]z sdf s s', '[b]z sdf s s'),
        ('[b][i]hello world![/b][/i]', '<strong>[i]hello world!</strong>[/i]'),
        ('[b]hello [i]world![/i]', '[b]hello <em>world!</em>'),
        ('[color]test[/color]', '[color]test[/color]'),
        ('[/abcdef][/i]', '[/abcdef][/i]'),
        ('[b\n hello [i]the[/i] world![/b]', '[b<br /> hello <em>the</em> world![/b]'),
        ('[b]hello [i]the[/b] world![/i]', '<strong>hello [i]the</strong> world![/i]'),
        ('[b] hello the[u]world ![/i] see you[/b]', '<strong> hello the[u]world ![/i] see you</strong>'),
        # BBCodes with semantic errors
        ('[color=some words]test[/color]', '[color=some words]test[/color]'),
        # Unknown BBCodes
        ('[unknown][hello][/unknown]', '[unknown][hello][/unknown]'),
    )

    CUSTOM_TAGS_RENDERING_TESTS = {
        'tags': {
            'justify': {
                'args': ('justify', '[justify]{TEXT}[/justify]', '<div style="text-align:justify;">{TEXT}</div>'),
                'kwargs': {},
            },
            'spoiler': {
                'args': ('spoiler', '[spoiler]{TEXT}[/spoiler]', '<div style="margin:20px; margin-top:5px"><div class="quotetitle"><strong> </strong>   <input type="button" value="Afficher" style="width:60px;font-size:10px;margin:0px;padding:0px;" onclick="if (this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display != '') { this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display = '';        this.innerText = ''; this.value = \'Masquer\'; } else { this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display = \'none\'; this.innerText = ''; this.value = \'Afficher\'; }" /></div><div class="quotecontent"><div style="display: none;">{TEXT}</div></div></div>'),
                'kwargs': {},
            },
            'youtube': {
                'args': ('youtube', '[youtube]{TEXT}[/youtube]', '<object width="425" height="350"><param name="movie" value="http://www.youtube.com/v/{TEXT}"></param><param name="wmode" value="transparent"></param><embed src="http://www.youtube.com/v/{TEXT}" type="application/x-shockwave-flash" wmode="transparent" width="425" height="350"></embed></object>'),
                'kwargs': {},
            },
            'h1': {
                'args': ('h1', '[h1={COLOR}]{TEXT}[/h1]', '<span style="border-left:6px {COLOR} solid;border-bottom:1px {COLOR} dotted;margin-left:8px;padding-left:4px;font-variant:small-caps;font-familly:Arial;font-weight:bold;font-size:150%;letter-spacing:0.2em;color:{COLOR};">{TEXT}</span><br />'),
                'kwargs': {},
            },
            'hr': {
                'args': ('hr', '[hr]', '<hr />'),
                'kwargs': {'standalone': True},
            },
            'size': {
                'args': ('size', '[size={NUMBER}]{TEXT}[/size]', '<span style="font-size:{NUMBER}px;">{TEXT}</span>'),
                'kwargs': {},
            },
            'mailto': {
                'args': ('email', '[email]{EMAIL}[/email]', '<a href="mailto:{EMAIL}">{EMAIL}</a>'),
                'kwargs': {'replace_links': False},
            },
            'simpletext': {
                'args': ('simpletext', '[simpletext]{SIMPLETEXT}[/simpletext]', '<span>{SIMPLETEXT}</span>'),
                'kwargs': {},
            }
        },
        'tests': (
            # BBcodes without errors
            ('[justify]hello world![/justify]', '<div style="text-align:justify;">hello world!</div>'),
            ('[spoiler]hidden![/spoiler]', '<div style="margin:20px; margin-top:5px"><div class="quotetitle"><strong> </strong>   <input type="button" value="Afficher" style="width:60px;font-size:10px;margin:0px;padding:0px;" onclick="if (this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display != '') { this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display = '';        this.innerText = ''; this.value = \'Masquer\'; } else { this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display = \'none\'; this.innerText = ''; this.value = \'Afficher\'; }" /></div><div class="quotecontent"><div style="display: none;">hidden!</div></div></div>'),
            ('[youtube]ztD3mRMdqSw[/youtube]', '<object width="425" height="350"><param name="movie" value="http://www.youtube.com/v/ztD3mRMdqSw"></param><param name="wmode" value="transparent"></param><embed src="http://www.youtube.com/v/ztD3mRMdqSw" type="application/x-shockwave-flash" wmode="transparent" width="425" height="350"></embed></object>'),
            ('[h1=#FFF]hello world![/h1]', '<span style="border-left:6px #FFF solid;border-bottom:1px #FFF dotted;margin-left:8px;padding-left:4px;font-variant:small-caps;font-familly:Arial;font-weight:bold;font-size:150%;letter-spacing:0.2em;color:#FFF;">hello world!</span><br />'),
            ('[hr]', '<hr />'),
            ('[size=24]hello world![/size]', '<span style="font-size:24px;">hello world!</span>'),
            ('[email]xyz@xyz.com[/email]', '<a href="mailto:xyz@xyz.com">xyz@xyz.com</a>'),
            ('[email]xyz.fr@xyz.com[/email]', '<a href="mailto:xyz.fr@xyz.com">xyz.fr@xyz.com</a>'),
            ('[simpletext]hello world[/simpletext]', '<span>hello world</span>'),
            # BBCodes with semantic errors
            ('[size=]hello world![/size]', '[size]hello world![/size]'),
            ('[size=hello]hello world![/size]', '[size=hello]hello world![/size]'),
            ('[email]hello world![/email]', '[email]hello world![/email]'),
            ('[email]http://www.google.com[/email]', '[email]http://www.google.com[/email]'),
            ('[email=12]24[/email]', '[email]24[/email]'),
            ('[simpletext]hello world![/simpletext]', '[simpletext]hello world![/simpletext]'),
            ('[simpletext]hello #~ world[/simpletext]', '[simpletext]hello #~ world[/simpletext]'),
        )
    }

    PLACEHOLDERS_RE_TESTS = {
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
            're': _url_re,
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

    def test_default_tags_rendering(self):
        # Run & check
        for bbcodes_text, expected_html_text in self.DEFAULT_TAGS_RENDERING_TESTS:
            result = self.parser.render(bbcodes_text)
            self.assertEqual(result, expected_html_text)

    def test_custom_tags_rendering(self):
        # Setup
        for _, tag_def in self.CUSTOM_TAGS_RENDERING_TESTS['tags'].items():
            self.parser.add_default_renderer(*tag_def['args'], **tag_def['kwargs'])
        # Run & check
        for bbcodes_text, expected_html_text in self.CUSTOM_TAGS_RENDERING_TESTS['tests']:
            result = self.parser.render(bbcodes_text)
            self.assertEqual(result, expected_html_text)

    def test_unicode_inputs(self):
        # Setup
        src = '[center]ƒünk¥ 你好 • §tüƒƒ 你好[/center]'
        dst = '<div style="text-align:center;">ƒünk¥ 你好 • §tüƒƒ 你好</div>'
        # Run & check
        self.assertEqual(self.parser.render(src), dst)

    def test_placeholder_regex(self):
        # Run & check
        for _, re_tests in self.PLACEHOLDERS_RE_TESTS.items():
            for test in re_tests['tests']:
                self.assertIsNotNone(re.search(re_tests['re'], test))
