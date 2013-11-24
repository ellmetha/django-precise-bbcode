# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
from collections import defaultdict
import re

# Third party imports
from django.db.models import get_model

# Local application / specific library imports
from .conf import settings as bbcode_settings


# BBCode regex
bbcodde_standard_re = r"^\[(?P<start_name>[A-Za-z0-9]*)(=\{[A-Za-z0-9]*\})?\]\{[A-Za-z0-9]*\}\[/(?P<end_name>[A-Za-z0-9]*)\]$"
bbcodde_standalone_re = r"^\[(?P<start_name>[A-Za-z0-9]*)(=\{[A-Za-z0-9]*\})?\]\{?[A-Za-z0-9]*\}?$"
bbcode_content_re = re.compile(r'^\[[A-Za-z0-9]*\](?P<content>.*)\[/[A-Za-z0-9]*\]')

# Other regex
placeholder_re = re.compile(r'{(\w+)}')
_url_re = re.compile(r'(?im)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\([^\s()<>]+\))+(?:\([^\s()<>]+\)|[^\s`!()\[\]{};:\'".,<>?]))')
_domain_re = re.compile(r'^(?=.{4,255}$)([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9]\.)+[a-zA-Z0-9]{2,5}$')
_email_re = re.compile(r'(\w+[.|\w])*@\[?(\w+[.])*\w+\]?', re.IGNORECASE)
_text_re = re.compile(r'^\s*([\w]+)|([\w]+\S*)\s*$', flags=re.UNICODE)
_simpletext_re = re.compile(r'^[a-zA-Z0-9-+.,_ ]+$')
_color_re = re.compile(r'^([a-z]+|#[0-9abcdefABCDEF]{3,6})$')
_number_re = re.compile(r'^[+-]?\d+(?:(\.|,)\d+)?$')


class InvalidBBCodePlaholder(Exception):
    pass


class BBCodeTagOptions(object):
    # Force the closing of this tag after a newline
    newline_closes = False
    # Force the closing of this tag after the start of the same tag
    same_tag_closes = False
    # Force the closing of this tag after the end of another tag
    end_tag_closes = False
    # This tag does not have a closing tag
    standalone = False
    # The embedded tags will be rendered
    render_embedded = True
    # The embedded newlines will be converted to markup
    transform_newlines = True
    # The HTML characters inside this tag will be escaped
    escape_html = True
    # Replace URLs with link markups inside this tag
    replace_links = True
    # Strip leading and trailing whitespace inside this tag
    strip = False
    # Swallow the first trailing newline
    swallow_trailing_newline = False

    # The following options will be usefull for BBCode editors
    helpline = None
    display_on_editor = True

    def __init__(self, **kwargs):
        for attr, value in list(kwargs.items()):
            setattr(self, attr, bool(value))


class BBCodeToken(object):
    TK_START_TAG = "start_tag"
    TK_END_TAG = "end_tag"
    TK_DATA = "data"
    TK_NEWLINE = "newline"

    def __init__(self, type, tag_name, option, text):
        self.type = type
        self.tag_name = tag_name
        self.option = option
        self.text = text

    def __repr__(self):
        return '<BBCodeToken instance "({0}, {1}, {2}, {3})">'.format(self.type, self.tag_name, self.option, self.text)

    def __unicode__(self):
        return 'BBCodeToken: ({0}, {1}, {2}, {3})'.format(self.type, self.tag_name, self.option, self.text)


class BBCodeParser(object):
    # A list of the default BBCode tags handled by the parser
    DEFAULT_TAGS = ('b', 'i', 'u', 's', 'list', '*', 'code', 'quote', 'center', 'color', 'url', 'img')

    # A list of all placeholder types supported by the parser and their corresponding regex
    PLACEHOLDERS_RE = {
        'URL': _url_re,
        'EMAIL': _email_re,
        'TEXT': _text_re,
        'SIMPLETEXT': _simpletext_re,
        'COLOR': _color_re,
        'NUMBER': _number_re,
    }

    # BBCode tags are enclosed in square brackets [ and ] rather than < and > ; the following constants should not be modified
    _TAG_OPENING = '['
    _TAG_ENDING = ']'

    def __init__(self, *args, **kwargs):
        self.newline_char = bbcode_settings.BBCODE_NEWLINE
        self.replace_html = bbcode_settings.BBCODE_ESCAPE_HTML
        self.normalize_newlines = bbcode_settings.BBCODE_NORMALIZE_NEWLINES
        self.bbcodes = {}
        # Init default renderers
        self.init_renderers()

    def add_renderer(self, tag_name, render_func, **kwargs):
        """
        Installs a renderer for the specified tag. A renderer is a function defined
        by the following signature:

        def render(tag_name, value, option=None, parent=None)

            tag_name
                The name of the tag being rendered.
            value
                The context between start and end tags, or None for standalone tags.
                Whether this has been rendered depends on render_embedded tag option.
            option
                The value of an option passed to the tag.
            parent
                The parent BBCodeTagOptions, if the tag is being rendered inside another tag,
                otherwise None.
        """
        options = BBCodeTagOptions(**kwargs)
        self.bbcodes[tag_name] = (render_func, options)

    def add_default_renderer(self, tag_name, tag_def, format_string, **kwargs):
        """
        Installs a renderer that constructs a dictionary composed of the value of the
        tag and its possible option and use it to semantically validate the tag and to
        format the rendered string.
        """
        def _render_default(name, value, option=None, parent=None):
            placeholders = re.findall(placeholder_re, tag_def)
            # Get the format data
            fmt = {}
            if len(placeholders) == 1:
                fmt.update({placeholders[0]: value})
            elif len(placeholders) == 2:
                fmt.update({placeholders[1]: value, placeholders[0]: self._replace(option, self.replace_html) if option else ''})

            # Semantic validation
            valid = self._validate_format(fmt)
            if not valid and option:
                return tag_def.format(**fmt)
            elif not valid:
                return tag_def.replace('=', '').format(**fmt)

            # Before rendering, it's necessary to escape the included braces: '{' and '}' ; some of them could not be placeholders
            escaped_format_string = format_string.replace('{', '{{').replace('}', '}}')
            for placeholder in fmt.keys():
                escaped_format_string = escaped_format_string.replace('{' + placeholder + '}', placeholder)

            # Return the rendered data
            return escaped_format_string.format(**fmt)
        self.add_renderer(tag_name, _render_default, **kwargs)

    def init_renderers(self):
        """
        Initializes some renderers for the default bbcode tags:

            b, i, u, s, list (and \*), code, quote, center, color, url and img
        """
        def _render_list(name, value, option=None, parent=None):
            css_opts = {
                '1': 'decimal', '01': 'decimal-leading-zero',
                'a': 'lower-alpha', 'A': 'upper-alpha',
                'i': 'lower-roman', 'I': 'upper-roman',
            }
            list_tag = 'ol' if option in css_opts else 'ul'
            list_tag_css = ' style="list-style-type:{};"'.format(css_opts[option]) if list_tag == 'ol' else ''
            rendered = '<{tag}{css}>{content}</{tag}>'.format(tag=list_tag, css=list_tag_css, content=value)
            return rendered

        def _render_url(name, value, option=None, parent=None):
            href = self._replace(option, self.replace_html) if option else value
            if '://' not in href and _domain_re.match(href):
                href = 'http://' + href
            content = value if option else href
            # Render
            return '<a href="{}">{}</a>'.format(href, content or href)

        self.add_default_renderer('b', '[b]{TEXT}[/b]', '<strong>{TEXT}</strong>')
        self.add_default_renderer('i', '[i]{TEXT}[/i]', '<em>{TEXT}</em>')
        self.add_default_renderer('u', '[u]{TEXT}[/u]', '<u>{TEXT}</u>')
        self.add_default_renderer('s', '[s]{TEXT}[/s]', '<strike>{TEXT}</strike>')
        self.add_renderer('list', _render_list, transform_newlines=True, strip=True)
        self.add_default_renderer('*', '[*]{TEXT}', '<li>{TEXT}</li>', newline_closes=True, same_tag_closes=True, end_tag_closes=True, strip=True)
        self.add_default_renderer('quote', '[quote]{TEXT}[/quote]', '<blockquote>{TEXT}</blockquote>', strip=True)
        self.add_default_renderer('code', '[code]{TEXT}[/code]', '<code>{TEXT}</code>', render_embedded=False)
        self.add_default_renderer('center', '[center]{TEXT}[/center]', '<div style="text-align:center;">{TEXT}</div>')
        self.add_default_renderer('color', '[color={COLOR}]{TEXT}[/color]', '<span style="color:{COLOR};">{TEXT}</span>')
        self.add_renderer('url', _render_url, replace_links=False)
        self.add_default_renderer('img', '[img]{URL}[/img]', '<img src="{URL}" alt="" />', replace_links=False)

    def _validate_format(self, format_dict):
        """
        Validates the given format dictionary. Each key of this dict refers to a specific BBCode placeholder type.
        eg. {TEXT} or {TEXT1} refer to the 'TEXT' BBCode placeholder type.
        Each content is validated according to its associated placeholder type.
        """
        for placeholder_name, content in format_dict.items():
            placeholder_type = re.sub('\d+$', '', placeholder_name)
            try:
                valid_content = re.search(self.PLACEHOLDERS_RE[placeholder_type], content)
                assert valid_content is not None
            except KeyError:
                raise InvalidBBCodePlaholder(placeholder_type)
            except AssertionError:
                return False
        return True

    def _parse_tag(self, tag):
        """
        Given a string assumed to be an opening tag or a ending tag, validates it and return a 4-tuple of the form:
            (valid, tag_name, closing, option)
        """
        # Validates the considered tag
        if ((not (tag.startswith(self._TAG_OPENING) and tag.endswith(self._TAG_ENDING))) or ('\n' in tag) or ('\r' in tag)
                or (tag.count(self._TAG_OPENING) > 1) or (tag.count(self._TAG_ENDING) > 1)):
            return (False, tag, False, None)
        tag_name = tag[len(self._TAG_OPENING):-len(self._TAG_ENDING)].strip()
        if not tag_name:
            return (False, tag, False, None)
        # Determines whether the tag is a closing tag or not
        closing = False
        option = None
        if tag_name.startswith('/'):
            tag_name = tag_name[1:]
            closing = True
        # Parses the option inside the tag
        if ('=' in tag_name) and closing:
            return (False, tag, False, None)
        elif ('=' in tag_name):
            option_pos = tag_name.find('=')
            option = tag_name[option_pos + 1:]
            tag_name = tag_name[:option_pos]
        return (True, tag_name.strip().lower(), closing, option)

    def get_tokens(self, data):
        """
        Acts as a lexer: given an input text, converts a sequence of characters into a sequence of tokens that represents
        the ramifications of the nested BBCode tags.
        Each token embeds the following data:

            Token type
                It can be: START_TAG, END_TAG, DATA, NEWLINE
            Tag name
                The name of the tokenized tag if a tag is considered, defaults to None
            Tag option
                The content of the tag option if available, defaults to None
            Token text
                The original text of the token
        """
        tokens = []
        pos = tag_start = tag_end = 0

        if self.normalize_newlines:
            data = data.replace('\r\n', '\n').replace('\r', '\n')
        while pos < len(data):
            # Search a new tag from the current position
            tag_start = data.find(self._TAG_OPENING, pos)
            pos_diff = tag_start - pos

            if pos_diff >= 0:
                # There can be data between the index of the current tag opening character and the previous position
                # These textual data are tokenised
                if pos_diff:
                    tokens.extend(self._get_textual_tokens(data[pos:tag_start]))

                # Try to find the apparent end of the current tag
                tag_end = data.find(self._TAG_ENDING, tag_start)
                # Is a new tag starting from here?
                new_tag_start = data.find(self._TAG_OPENING, tag_start + len(self._TAG_OPENING))

                if new_tag_start > 0 and new_tag_start < tag_end:
                    # In this case, a new opening character has been found ; the previous ones will be tokenized as data.
                    tokens.extend(self._get_textual_tokens(data[tag_start:new_tag_start]))
                    pos = new_tag_start
                elif tag_end > tag_start:
                    tag = data[tag_start:tag_end + len(self._TAG_ENDING)]
                    valid, tag_name, closing, option = self._parse_tag(tag)
                    # The fetched tag must be known by the parser to be tokenized as a BBCode tag ; otherwise it will be tokenized as data
                    if valid and tag_name in self.bbcodes:
                        if closing:
                            tokens.append(BBCodeToken(BBCodeToken.TK_END_TAG, tag_name, None, tag))
                        else:
                            tokens.append(BBCodeToken(BBCodeToken.TK_START_TAG, tag_name, option, tag))
                    else:
                        tokens.extend(self._get_textual_tokens(tag))
                    pos = tag_end + len(self._TAG_ENDING)
                else:
                    # An umatched [
                    break
            else:
                break
        # Tokenize the remaining data if a break occured
        if pos < len(data):
            tokens.extend(self._get_textual_tokens(data[pos:]))
        return tokens

    def _get_textual_tokens(self, data):
        """
        Given a list of textual data, returns a list of TK_NEWLINE or TK_DATA tokens.
        """
        token_types = []
        token_types = defaultdict(lambda: BBCodeToken.TK_DATA, token_types)
        token_types['\n'] = BBCodeToken.TK_NEWLINE
        tokens = []

        data = re.split('(\n)', data)
        for value in data:
            if value:
                tokens.append(BBCodeToken(token_types[value], None, None, value))
        return tokens

    def _drop_syntactic_errors(self, tokens):
        """
        Given a list of lexical tokens, find the tags that are not closed or not started and converts them to textual tokens.
        The non-valid tokens must not be swallowed. The tag tokens that are not valid in the BBCode tree will be converted to
        textual tokens (eg. in '[b][i]test[/b][/i]' the 'b' tags will be tokenized as data).
        """
        opening_tags = []
        for index, token in enumerate(tokens):
            if token.type == BBCodeToken.TK_START_TAG:
                _, tag_options = self.bbcodes[token.tag_name]
                if tag_options.same_tag_closes and len(opening_tags) > 0 and opening_tags[-1][0].tag_name == token.tag_name:
                    opening_tags.pop()
                if not tag_options.standalone:
                    opening_tags.append((token, index))
            elif token.type == BBCodeToken.TK_END_TAG:
                _, tag_options = self.bbcodes[token.tag_name]
                if len(opening_tags) > 0:
                    previous_tag, _ = opening_tags[-1]
                    _, previous_tag_options = self.bbcodes[previous_tag.tag_name]
                    if previous_tag_options.end_tag_closes:
                        opening_tags.pop()

                    if not opening_tags:
                        continue

                    if (opening_tags[-1][0].tag_name != token.tag_name and token.tag_name in [x[0].tag_name for x in opening_tags]
                            and tag_options.render_embedded):
                        # In this case, we iterate to the first opening of the current tag : all the tags between the current tag
                        # and its opening are converted to textual tokens
                        for tag in reversed(opening_tags):
                            tk, index = tag
                            if tk.tag_name == token.tag_name:
                                opening_tags.pop()
                                break
                            else:
                                tokens[index] = BBCodeToken(BBCodeToken.TK_DATA, None, None, tk.text)
                                opening_tags.pop()
                    elif opening_tags[-1][0].tag_name != token.tag_name:
                        tokens[index] = BBCodeToken(BBCodeToken.TK_DATA, None, None, token.text)
                    else:
                        opening_tags.pop()
                else:
                    tokens[index] = BBCodeToken(BBCodeToken.TK_DATA, None, None, token.text)
            elif token.type == BBCodeToken.TK_NEWLINE:
                if len(opening_tags) > 0:
                    previous_tag, _ = opening_tags[-1]
                else:
                    previous_tag = None
                if previous_tag:
                    _, previous_tag_options = self.bbcodes[previous_tag.tag_name]
                    if previous_tag_options.newline_closes:
                        opening_tags.pop()
        # The remaining tags do not have a closing tag, they must be converted to testual tokens)
        for tag in opening_tags:
            token, index = tag
            tokens[index] = BBCodeToken(BBCodeToken.TK_DATA, None, None, token.text)
        return tokens

    def _print_lexical_token_stream(self, data):  # pragma: no cover
        """
        Given an input text, print out the lexical token stream.
        """
        tokens = self._drop_syntactic_errors(self.get_tokens(data))
        for tk in tokens:
            if tk.type in [BBCodeToken.TK_START_TAG, BBCodeToken.TK_END_TAG]:
                if tk.option:
                    print(tk.type.upper() + " " + tk.tag_name + ", option = \"" + tk.option + "\"")
                else:
                    print(tk.type.upper() + " " + tk.tag_name)
            elif tk.type == BBCodeToken.TK_DATA:
                print(tk.type.upper() + " \"" + tk.text + "\"")
            elif tk.type == BBCodeToken.TK_NEWLINE:
                print(tk.type.upper())

    def _find_closing_token(self, tag_name, tag_options, tokens, pos):
        """
        Given the name and the options of a considered tag, a list of lexical tokens and the position of the current tag in this list,
        find the position of the associated closing tag. This function returns a tuple of the form (end_pos, consume_now), where 'consume_now'
        is a boolean that indicates whether the ending token should be consumed or not.
        """
        similar_tags_embedded = 0
        while pos < len(tokens):
            token = tokens[pos]
            if token.type == BBCodeToken.TK_NEWLINE and tag_options.newline_closes:
                return pos, True
            elif token.type == BBCodeToken.TK_START_TAG and token.tag_name == tag_name:
                if tag_options.same_tag_closes:
                    return pos, False
                if tag_options.render_embedded:
                    similar_tags_embedded += 1
            elif token.type == BBCodeToken.TK_END_TAG and token.tag_name == tag_name:
                if similar_tags_embedded > 0:
                    similar_tags_embedded -= 1
                else:
                    return pos, True
            pos += 1
        return pos, True

    def _render_tokens(self, tokens, parent_tag=None):
        """
        Given a list of lexical tokens, do the rendering process. During this process, some semantic verifications
        are done on this lexical token stream.
        """
        itk = 0
        rendered = []
        while itk < len(tokens):
            # Fetch the considered token
            token = tokens[itk]

            # Try to render it according to its type
            if token.type == BBCodeToken.TK_START_TAG:
                # Fetch some data about the current tag
                call_rendering_function, tag_options = self.bbcodes[token.tag_name]

                if tag_options.standalone:
                    rendered.append(call_rendering_function(token.tag_name, None, token.option, parent_tag))
                else:
                    # First find the closing tag associated with this tag
                    token_end, consume_now = self._find_closing_token(token.tag_name, tag_options, tokens, itk + 1)
                    embedded_tokens = tokens[itk + 1:token_end]

                    # If the end tag should not be consumed, back up one (after processing the embedded tokens)
                    if not consume_now:
                        token_end -= 1

                    if tag_options.render_embedded:
                        inner = self._render_tokens(embedded_tokens, parent_tag=tag_options)
                    else:
                        inner = self._render_textual_content(''.join(tk.text for tk in embedded_tokens),
                                                             tag_options.escape_html, tag_options.replace_links)

                    # Strip and replaces newlines if specified in the tag options
                    if tag_options.strip:
                        inner = inner.strip()
                    if tag_options.transform_newlines:
                        inner = inner.replace('\n', self.newline_char)

                    # Append the rendered data
                    rendered.append(call_rendering_function(token.tag_name, inner, token.option, parent_tag))

                    # Swallow the first trailing newline if necessary
                    if tag_options.swallow_trailing_newline:
                        next_itk = token_end + 1
                        if next_itk < len(tokens) and tokens[next_itk].type == BBCodeToken.TK_NEWLINE:
                            token_end = next_itk

                    # Goto the end tag index
                    itk = token_end
            elif token.type == BBCodeToken.TK_DATA:
                replace_specialchars = parent_tag.escape_html if parent_tag else True
                replace_links = parent_tag.replace_links if parent_tag else True
                rendered.append(self._render_textual_content(token.text, replace_specialchars, replace_links))
            elif token.type == BBCodeToken.TK_NEWLINE:
                rendered.append(self.newline_char if parent_tag is None else token.text)

            # Goto the next token!
            itk += 1
        return ''.join(rendered)

    def _render_textual_content(self, data, replace_specialchars, replace_links):
        """
        Given an input text, update it by replacing the HTML special characters or the found links by their HTML corresponding.
        """
        url_matches = []

        if replace_links:
            # The links must be pulled out before doing any character replacement
            pos = 0
            while True:
                match = _url_re.search(data, pos)
                if not match:
                    break
                # Replace any link with a token that will be substitude back after replacements
                token = '-*-bbcode-link-{match}-{pos}-*-'.format(match=id(match), pos=pos)
                url_matches.append((token, self._link_replace(match)))
                url_start, url_end = match.span()
                data = data[:url_start] + token + data[url_end:]
                pos = url_start
        if replace_specialchars:
            data = self._replace(data, self.replace_html)
        # Now put the previously genered links in the result text
        for token, replacement in url_matches:
            data = data.replace(token, replacement)
        return data

    def _link_replace(self, match):
        """
        Callback for re.sub to replace textual links with HTML links.
        """
        url = match.group(0)
        href = url
        if '://' not in href:
            href = 'http://' + href
        return '<a href="{0}">{1}</a>'.format(href, url)

    def _replace(self, data, replacements):
        """
        Given a list of 2-tuples (old, new), performs all replacements on the data and
        returns the result.
        """
        for old, new in replacements:
            data = data.replace(old, new)
        return data

    def render(self, data):
        """
        Renders the given data by using the declared BBCodes tags.
        """
        lexical_units = self._drop_syntactic_errors(self.get_tokens(data))
        rendered = self._render_tokens(lexical_units)
        return rendered


_bbcode_parser = None
# The easiest way to use the BBcode parser is to import the following get_parser function (except if
# you need many BBCodeParser instances at a time or you want to subclass it).
# 
# Note if you create a new instance of BBCodeParser, the built in bbcode tags are still installed.


def get_parser():
    if not _bbcode_parser:
        _load_parser()
    return _bbcode_parser


def _init_bbcode_tags(parser):
    """
    Call the BBCode tag pool to fetch all the module-based tags and initializes
    their associated renderers.
    """
    from precise_bbcode.tag_pool import tag_pool
    tags = tag_pool.get_tags()
    for tag_def in tags:
        tag = tag_def()
        parser.add_renderer(tag.tag_name, tag.render, **tag._options())


def _init_custom_bbcode_tags(parser):
    """
    Find the user-defined BBCode tags and initializes their associated renderers.
    """
    BBCodeTag = get_model('precise_bbcode', 'BBCodeTag')
    if BBCodeTag:
        custom_tags = BBCodeTag.objects.all()
        for tag in custom_tags:
            args, kwargs = tag.parser_args
            parser.add_default_renderer(*args, **kwargs)


def _load_parser():
    global _bbcode_parser
    _bbcode_parser = BBCodeParser()

    # Init renderers registered in 'bbcode_tags' modules
    _init_bbcode_tags(_bbcode_parser)

    # Init custom renderers defined in BBCodeTag model instances
    if bbcode_settings.BBCODE_ALLOW_CUSTOM_TAGS:
        _init_custom_bbcode_tags(_bbcode_parser)
