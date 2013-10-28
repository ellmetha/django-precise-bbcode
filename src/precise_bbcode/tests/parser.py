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
        ('[b]hello [i]world![/i][/b]', '<strong>hello <em>world!</em></strong>'),
        ('[b]hello [ world![/b]', '<strong>hello [ world!</strong>'),
        ('[b]]he[llo [ w]orld![/b]', '<strong>]he[llo [ w]orld!</strong>'),
        ('[ b ]hello [u]world![/u][ /b ]', '<strong>hello <u>world!</u></strong>'),
        ('[b]hello [] world![/b]', '<strong>hello [] world!</strong>'),
        ('[list]\n[*]one\n[*]two\n[/list]', '<ul><li>one</li><li>two</li></ul>'),
        ('[list=1]\n[*]item 1\n[*]item 2\n[/list]', '<ol style="list-style-type:decimal;"><li>item 1</li><li>item 2</li></ol>'),
        ('>> some special chars >< <>', '&gt;&gt; some special chars &gt;&lt; &lt;&gt;'),
        ('"quoted text"', '&quot;quoted text&quot;'),
        ('>> some other special chars', '&gt;&gt; some other special chars'),
        ('[url]http://foo.com/bar.php?some--data[/url]', '<a href="http://foo.com/bar.php?some--data">http://foo.com/bar.php?some--data</a>'),
        ('[url]http://www.google.com[/url]', '<a href="http://www.google.com">http://www.google.com</a>'),
        ('[url=google.com]goto google[/url]', '<a href="http://google.com">goto google</a>'),
        ('[url=http://google.com][/url]', '<a href="http://google.com">http://google.com</a>'),
        ('www.google.com foo.com/bar http://xyz.ci', '<a href="http://www.google.com">www.google.com</a> <a href="http://foo.com/bar">foo.com/bar</a> <a href="http://xyz.ci">http://xyz.ci</a>'),
        ('[color=green]goto [url=google.com]google website[/url][/color]', '<span style="color:green;">goto <a href="http://google.com">google website</a></span>'),
        ('[quote] \r\nhello\nworld! [/quote]', '<blockquote>hello<br />world!</blockquote>'),
        ('[color=#FFFFFF]white[/color]', '<span style="color:#FFFFFF;">white</span>'),
        ('[url=<script>alert(1);</script>]xss[/url]', '<a href="http://&lt;script&gt;alert(1);&lt;/script&gt;">xss</a>'),
        ('[color=<script></script>]xss[/color]', '[color=&lt;script&gt;&lt;/script&gt;]xss[/color]'),
        # BBCodes with syntactic errors
        ('[b]z sdf s s', '[b]z sdf s s'),
        ('[b][i]hello world![/b][/i]', '[b]<em>hello world![/b]</em>'),
        ('[b]hello [i]world![/i]', '[b]hello <em>world!</em>'),
        ('[color]test[/color]', '[color]test[/color]'),
        ('[/abcdef][/i]', '[/abcdef][/i]'),
        ('[b\n hello [i]the[/i] world![/b]', '[b<br /> hello <em>the</em> world![/b]'),
        ('[b]hello [i]the[/b] world![/i]', '[b]hello <em>the[/b] world!</em>'),
        # BBCodes with semantic errors
        # Unknown BBCodes
        ('[unknown][hello][/unknown]', '[unknown][hello][/unknown]'),
    )

    def setUp(self):
        self.parser = BBCodeParser()

    def test_rendering(self):
        # Run & check
        for bbcodes_text, expected_html_text in self.RENDERING_TESTS:
            result = self.parser.render(bbcodes_text)
            self.assertEqual(result, expected_html_text)
