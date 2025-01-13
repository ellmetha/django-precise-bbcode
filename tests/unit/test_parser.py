from precise_bbcode.bbcode import get_parser
from precise_bbcode.test import gen_bbcode_tag_klass


class TestParser(object):
    DEFAULT_TAGS_RENDERING_TESTS = (
        # BBcodes without errors
        ('[b]hello world![/b]', '<strong>hello world!</strong>'),
        ('[b]hello [i]world![/i][/b]', '<strong>hello <em>world!</em></strong>'),
        ('[b]hello [ world![/b]', '<strong>hello [ world!</strong>'),
        ('[b]]he[llo [ w]orld![/b]', '<strong>]he[llo [ w]orld!</strong>'),
        ('[b]]hello [b]the[/b] world![/b]', '<strong>]hello <strong>the</strong> world!</strong>'),
        ('[ b ]hello [u]world![/u][ /b ]', '<strong>hello <u>world!</u></strong>'),
        ('[b]hello [] world![/b]', '<strong>hello [] world!</strong>'),
        ('[list]\n[*]one\n[*]two\n[/list]', '<ul><li>one</li><li>two</li></ul>'),
        (
            '[list=1]\n[*]item 1\n[*]item 2\n[/list]',
            '<ol style="list-style-type:decimal;"><li>item 1</li><li>item 2</li></ol>'
        ),
        (
            '[list] [*]Item 1 [*]Item 2 [*]Item 3   [/list]',
            '<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>'
        ),
        ('>> some special chars >< <>', '&gt;&gt; some special chars &gt;&lt; &lt;&gt;'),
        ('"quoted text"', '&quot;quoted text&quot;'),
        ('>> some other special chars', '&gt;&gt; some other special chars'),
        (
            '[url]http://foo.com/bar.php?some--data[/url]',
            '<a href="http://foo.com/bar.php?some--data">http://foo.com/bar.php?some--data</a>'
        ),
        (
            '[url]http://www.google.com[/url]',
            '<a href="http://www.google.com">http://www.google.com</a>'
        ),
        ('[url=google.com]goto google[/url]', '<a href="http://google.com">goto google</a>'),
        ('[url=http://google.com][/url]', '<a href="http://google.com">http://google.com</a>'),
        ('[url=\'http://google.com\'][/url]', '<a href="http://google.com">http://google.com</a>'),
        ('[url="http://google.com"][/url]', '<a href="http://google.com">http://google.com</a>'),
        ('[URL=google.com]goto google[/URL]', '<a href="http://google.com">goto google</a>'),
        (
            '[url=<script>alert(1);</script>]xss[/url]',
            '[url=&lt;script&gt;alert(1);&lt;/script&gt;]xss[/url]'
        ),
        (
            'www.google.com foo.com/bar http://xyz.ci',
            '<a href="http://www.google.com">www.google.com</a> '
            '<a href="http://foo.com/bar">foo.com/bar</a> <a href="http://xyz.ci">http://xyz.ci</a>'
        ),
        ('[url=relative/foo/bar.html]link[/url]', '[url=relative/foo/bar.html]link[/url]'),
        ('[url=/absolute/foo/bar.html]link[/url]', '[url=/absolute/foo/bar.html]link[/url]'),
        ('[url=./hello.html]world![/url]', '[url=./hello.html]world![/url]'),
        (
            '[url=javascript:alert(String.fromCharCode(88,83,83))]http://google.com[/url]',
            '[url=javascript:alert(String.fromCharCode(88,83,83))]http://google.com[/url]'
        ),
        (
            '[url]http://google.com?[url] '
            'onmousemove=javascript:alert(String.fromCharCode(88,83,83));//[/url][/url]',
            '[url]http://google.com?[url] '
            'onmousemove=javascript:alert(String.fromCharCode(88,83,83));//[/url][/url]'
        ),
        (
            '[img]http://www.foo.com/bar/img.png[/img]',
            '<img src="http://www.foo.com/bar/img.png" alt="" />'
        ),
        (
            '[img]fake.png" onerror="alert(String.fromCharCode(88,83,83))[/img]',
            '[img]fake.png&quot; onerror&quot;alert(String.fromCharCode(88,83,83))[/img]'
        ),
        (
            '[img]http://foo.com/fake.png [img] '
            'onerror=javascript:alert(String.fromCharCode(88,83,83)) [/img] [/img]',
            '[img]http://foo.com/fake.png [img] '
            'onerrorjavascript:alert(String.fromCharCode(88,83,83)) [/img] [/img]'
        ),
        ('[quote] \r\nhello\nworld! [/quote]', '<blockquote>hello<br />world!</blockquote>'),
        ('[code][b]hello world![/b][/code]', '<code>[b]hello world![/b]</code>'),
        (
            '[color=green]goto [url=google.com]google website[/url][/color]',
            '<span style="color:green;">goto <a href="http://google.com">google website</a></span>'
        ),
        ('[color=#FFFFFF]white[/color]', '<span style="color:#FFFFFF;">white</span>'),
        (
            '[color=<script></script>]xss[/color]',
            '[color=&lt;script&gt;&lt;/script&gt;]xss[/color]'
        ),
        ('[COLOR=blue]hello world![/color]', '<span style="color:blue;">hello world!</span>'),
        (
            '[color=#ff0000;font-size:100px;]XSS[/color]',
            '[color=#ff0000;font-size:100px;]XSS[/color]'
        ),
        (
            '[color=#ff0000;xss:expression(alert(String.fromCharCode(88,83,83)));]XSS[/color]',
            '[color=#ff0000;xss:expression(alert(String.fromCharCode(88,83,83)));]XSS[/color]'
        ),
        ('[', '['),
        # BBCodes with syntactic errors
        ('[b]z sdf s s', '[b]z sdf s s'),
        ('[b][i]hello world![/b][/i]', '<strong>[i]hello world!</strong>[/i]'),
        ('[b]hello [i]world![/i]', '[b]hello <em>world!</em>'),
        ('[color]test[/color]', '[color]test[/color]'),
        ('[/abcdef][/i]', '[/abcdef][/i]'),
        ('[b\n hello [i]the[/i] world![/b]', '[b<br /> hello <em>the</em> world![/b]'),
        ('[b]hello [i]the[/b] world![/i]', '<strong>hello [i]the</strong> world![/i]'),
        (
            '[b] hello the[u]world ![/i] see you[/b]',
            '<strong> hello the[u]world ![/i] see you</strong>'
        ),
        ('[col\nor]more tests[/color]', '[col<br />or]more tests[/color]'),
        ('[color]more tests[/color=#FFF]', '[color]more tests[/color=#FFF]'),
        ('[*]hello[/i]', '<li>hello</li>'),
        ('[url=\'\']Hello[/url]', '[url=&#39;&#39;]Hello[/url]'),  # No url in quotes (empty url)
        ('[url=\'http://google.com][/url]',
         '[url=&#39;http://google.com][/url]'),  # Open quote but no close in url
        # BBCodes with semantic errors
        ('[color=some words]test[/color]', '[color=some words]test[/color]'),
        # Unknown BBCodes
        ('[unknown][hello][/unknown]', '[unknown][hello][/unknown]'),
        ('[url]"[url]', '[url]&quot;[url]'),
        ('[url="]wow, that is very short[url]', '[url=&quot;]wow, that is very short[url]'),
    )

    CUSTOM_TAGS_RENDERING_TESTS = {
        'tags': {
            'justify': {
                'Tag': {
                    'name': 'justify',
                    'definition_string': '[justify]{TEXT}[/justify]',
                    'format_string': '<div style="text-align:justify;">{TEXT}</div>',
                },
                'Options': {},
            },
            'spoiler': {
                'Tag': {
                    'name': 'spoiler',
                    'definition_string': '[spoiler]{TEXT}[/spoiler]',
                    'format_string': '<div style="margin:20px; margin-top:5px"><div class="quotetitle"><strong> </strong>   <input type="button" value="Afficher" style="width:60px;font-size:10px;margin:0px;padding:0px;" onclick="if (this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display != '') { this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display = '';        this.innerText = ''; this.value = \'Masquer\'; } else { this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display = \'none\'; this.innerText = ''; this.value = \'Afficher\'; }" /></div><div class="quotecontent"><div style="display: none;">{TEXT}</div></div></div>',  # noqa
                },
                'Options': {},
            },
            'youtube': {
                'Tag': {
                    'name': 'youtube',
                    'definition_string': '[youtube]{TEXT}[/youtube]',
                    'format_string': (
                        '<object width="425" height="350"><param name="movie" '
                        'value="http://www.youtube.com/v/{TEXT}"></param><param name="wmode" '
                        'value="transparent"></param><embed src="http://www.youtube.com/v/{TEXT}" '
                        'type="application/x-shockwave-flash" wmode="transparent" width="425" '
                        'height="350"></embed></object>'
                    ),
                },
                'Options': {},
            },
            'h1': {
                'Tag': {
                    'name': 'h1',
                    'definition_string': '[h1={COLOR}]{TEXT}[/h1]',
                    'format_string': (
                        '<span style="border-left:6px {COLOR} solid;border-bottom:1px {COLOR} '
                        'dotted;margin-left:8px;padding-left:4px;font-variant:small-caps;'
                        'font-familly:Arial;font-weight:bold;font-size:150%;letter-spacing:0.2em;'
                        'color:{COLOR};">{TEXT}</span><br />'
                    ),
                },
                'Options': {},
            },
            'hr': {
                'Tag': {
                    'name': 'hr',
                    'definition_string': '[hr]',
                    'format_string': '<hr />',
                },
                'Options': {'standalone': True},
            },
            'size': {
                'Tag': {
                    'name': 'size',
                    'definition_string': '[size={NUMBER}]{TEXT}[/size]',
                    'format_string': '<span style="font-size:{NUMBER}px;">{TEXT}</span>',
                },
                'Options': {},
            },
            'mailto': {
                'Tag': {
                    'name': 'email',
                    'definition_string': '[email]{EMAIL}[/email]',
                    'format_string': '<a href="mailto:{EMAIL}">{EMAIL}</a>',
                },
                'Options': {'replace_links': False},
            },
            'simpletext': {
                'Tag': {
                    'name': 'simpletext',
                    'definition_string': '[simpletext]{SIMPLETEXT}[/simpletext]',
                    'format_string': '<span>{SIMPLETEXT}</span>',
                },
                'Options': {},
            }
        },
        'tests': (
            # BBcodes without errors
            (
                '[justify]hello world![/justify]',
                '<div style="text-align:justify;">hello world!</div>'
            ),
            (
                '[spoiler]hidden![/spoiler]',
                '<div style="margin:20px; margin-top:5px"><div class="quotetitle"><strong> </strong>   <input type="button" value="Afficher" style="width:60px;font-size:10px;margin:0px;padding:0px;" onclick="if (this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display != '') { this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display = '';        this.innerText = ''; this.value = \'Masquer\'; } else { this.parentNode.parentNode.getElementsByTagName(\'div\')[1].getElementsByTagName(\'div\')[0].style.display = \'none\'; this.innerText = ''; this.value = \'Afficher\'; }" /></div><div class="quotecontent"><div style="display: none;">hidden!</div></div></div>'  # noqa
            ),
            (
                '[youtube]ztD3mRMdqSw[/youtube]',
                '<object width="425" height="350"><param name="movie" value="http://www.youtube.com/v/ztD3mRMdqSw"></param><param name="wmode" value="transparent"></param><embed src="http://www.youtube.com/v/ztD3mRMdqSw" type="application/x-shockwave-flash" wmode="transparent" width="425" height="350"></embed></object>'  # noqa
            ),
            (
                '[h1=#FFF]hello world![/h1]',
                '<span style="border-left:6px #FFF solid;border-bottom:1px #FFF dotted;margin-left:8px;padding-left:4px;font-variant:small-caps;font-familly:Arial;font-weight:bold;font-size:150%;letter-spacing:0.2em;color:#FFF;">hello world!</span><br />'  # noqa
            ),
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

    def setup_method(self, method):
        self.parser = get_parser()

    def test_can_render_default_tags(self):
        # Run & check
        for bbcodes_text, expected_html_text in self.DEFAULT_TAGS_RENDERING_TESTS:
            result = self.parser.render(bbcodes_text)
            assert result == expected_html_text

    def test_can_render_custom_tags(self):
        # Setup
        for _, tag_def in self.CUSTOM_TAGS_RENDERING_TESTS['tags'].items():
            self.parser.add_bbcode_tag(gen_bbcode_tag_klass(tag_def['Tag'], tag_def['Options']))
        # Run & check
        for bbcodes_text, expected_html_text in self.CUSTOM_TAGS_RENDERING_TESTS['tests']:
            result = self.parser.render(bbcodes_text)
            assert result == expected_html_text

    def test_can_handle_unicode_inputs(self):
        # Setup
        src = '[center]ƒünk¥ 你好 • §tüƒƒ 你好[/center]'
        dst = '<div style="text-align:center;">ƒünk¥ 你好 • §tüƒƒ 你好</div>'
        # Run & check
        assert self.parser.render(src) == dst
