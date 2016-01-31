# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import Client
import pytest

from precise_bbcode.bbcode import BBCodeParserLoader
from precise_bbcode.bbcode import get_parser
from precise_bbcode.bbcode.tag import BBCodeTag as ParserBBCodeTag
from precise_bbcode.bbcode.exceptions import InvalidBBCodePlaholder
from precise_bbcode.bbcode.exceptions import InvalidBBCodeTag
from precise_bbcode.models import BBCodeTag
from precise_bbcode.tag_pool import TagAlreadyCreated
from precise_bbcode.tag_pool import TagAlreadyRegistered
from precise_bbcode.tag_pool import TagNotRegistered
from precise_bbcode.tag_pool import tag_pool


class FooTag(ParserBBCodeTag):
    name = 'foo'

    class Options:
        render_embedded = False

    def render(self, value, option=None, parent=None):
        return '<pre>{}</pre>'.format(value)


class FooTagAlt(ParserBBCodeTag):
    name = 'fooalt'

    class Options:
        render_embedded = False

    def render(self, value, option=None, parent=None):
        return '<pre>{}</pre>'.format(value)


class FooTagSub(ParserBBCodeTag):
    name = 'foo2'

    class Options:
        render_embedded = False


class BarTag(ParserBBCodeTag):
    name = 'bar'

    def render(self, value, option=None, parent=None):
        if not option:
            return '<div class="bar">{}</div>'.format(value)
        return '<div class="bar" style="color:{};">{}</div>'.format(option, value)


@pytest.mark.django_db
class TestBbcodeTagPool(object):
    TAGS_TESTS = (
        ('[fooalt]hello world![/fooalt]', '<pre>hello world!</pre>'),
        ('[bar]hello world![/bar]', '<div class="bar">hello world!</div>'),
        ('[fooalt]hello [bar]world![/bar][/fooalt]', '<pre>hello [bar]world![/bar]</pre>'),
        ('[bar]hello [fooalt]world![/fooalt][/bar]', '<div class="bar">hello <pre>world!</pre></div>'),
        ('[bar]안녕하세요![/bar]', '<div class="bar">안녕하세요!</div>'),
    )

    def setup_method(self, method):
        self.parser = get_parser()

    def test_should_raise_if_a_tag_is_registered_twice(self):
        # Setup
        number_of_tags_before = len(tag_pool.get_tags())
        tag_pool.register_tag(FooTag)
        # Run & check
        # Let's add it a second time. We should catch an exception
        with pytest.raises(TagAlreadyRegistered):
            tag_pool.register_tag(FooTag)
        # Let's make sure we have the same number of tags as before
        tag_pool.unregister_tag(FooTag)
        number_of_tags_after = len(tag_pool.get_tags())
        assert number_of_tags_before == number_of_tags_after

    def test_cannot_register_tags_with_incorrect_parent_classes(self):
        # Setup
        number_of_tags_before = len(tag_pool.get_tags())
        # Run & check
        with pytest.raises(ImproperlyConfigured):
            class ErrnoneousTag4:
                pass
            tag_pool.register_tag(ErrnoneousTag4)
        number_of_tags_after = len(tag_pool.get_tags())
        assert number_of_tags_before == number_of_tags_after

    def test_cannot_register_tags_that_are_already_stored_in_the_database(self):
        # Setup
        BBCodeTag.objects.create(
            tag_definition='[tt]{TEXT}[/tt]', html_replacement='<span>{TEXT}</span>')
        # Run
        with pytest.raises(TagAlreadyCreated):
            class ErrnoneousTag9(ParserBBCodeTag):
                name = 'tt'
                definition_string = '[tt]{TEXT}[/tt]'
                format_string = '<span>{TEXT}</span>'
            tag_pool.register_tag(ErrnoneousTag9)

    def test_cannot_unregister_a_non_registered_tag(self):
        # Setup
        number_of_tags_before = len(tag_pool.get_tags())
        # Run & check
        with pytest.raises(TagNotRegistered):
            tag_pool.unregister_tag(FooTagSub)
        number_of_tags_after = len(tag_pool.get_tags())
        assert number_of_tags_before == number_of_tags_after

    def test_tags_can_be_rendered(self):
        # Setup
        parser_loader = BBCodeParserLoader(parser=self.parser)
        tag_pool.register_tag(FooTagAlt)
        tag_pool.register_tag(BarTag)
        parser_loader.init_bbcode_tags()
        # Run & check
        for bbcodes_text, expected_html_text in self.TAGS_TESTS:
            result = self.parser.render(bbcodes_text)
            assert result == expected_html_text


@pytest.mark.django_db
class TestBbcodeTag(object):
    def setup_method(self, method):
        self.parser = get_parser()

    def test_that_are_invalid_should_raise_at_runtime(self):
        # Run & check
        with pytest.raises(InvalidBBCodeTag):
            class ErrnoneousTag1(ParserBBCodeTag):
                pass
        with pytest.raises(InvalidBBCodeTag):
            class ErrnoneousTag2(ParserBBCodeTag):
                delattr(ParserBBCodeTag, 'name')
        with pytest.raises(InvalidBBCodeTag):
            class ErrnoneousTag3(ParserBBCodeTag):
                name = 'it\'s a bad tag name'
        with pytest.raises(InvalidBBCodeTag):
            class ErrnoneousTag4(ParserBBCodeTag):
                name = 'ooo'
                definition_string = '[ooo]{TEXT}[/ooo]'
        with pytest.raises(InvalidBBCodeTag):
            class ErrnoneousTag5(ParserBBCodeTag):
                name = 'ooo'
                definition_string = 'bad definition'
                format_string = 'bad format string'
        with pytest.raises(InvalidBBCodeTag):
            class ErrnoneousTag6(ParserBBCodeTag):
                name = 'ooo'
                definition_string = '[ooo]{TEXT}[/aaa]'
                format_string = 'bad format string'
        with pytest.raises(InvalidBBCodeTag):
            class ErrnoneousTag7(ParserBBCodeTag):
                name = 'ooo'
                definition_string = '[ooo]{TEXT}[/ooo]'
                format_string = '<span></span>'
        with pytest.raises(InvalidBBCodeTag):
            class ErrnoneousTag8(ParserBBCodeTag):
                name = 'ooo'
                definition_string = '[ooo={TEXT}]{TEXT}[/ooo]'
                format_string = '<span>{TEXT}</span>'

    def test_containing_invalid_placeholders_should_raise_during_rendering(self):
        # Setup
        class TagWithInvalidPlaceholders(ParserBBCodeTag):
            name = 'bad'
            definition_string = '[bad]{FOOD}[/bad]'
            format_string = '<span>{FOOD}</span>'
        self.parser.add_bbcode_tag(TagWithInvalidPlaceholders)
        # Run
        with pytest.raises(InvalidBBCodePlaholder):
            self.parser.render('[bad]apple[/bad]')


@pytest.mark.django_db
class TestDbBbcodeTag(object):
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
        {'tag_definition': '[bar]{TEXT}[/bar]', 'html_replacement': '<span>{TEXT}</span>'},  # Already registered
    )

    VALID_TAG_TESTS = (
        {'tag_definition': '[pre]{TEXT}[/pre]', 'html_replacement': '<pre>{TEXT}</pre>'},
        {'tag_definition': '[pre2={COLOR}]{TEXT1}[/pre2]', 'html_replacement': '<pre style="color:{COLOR};">{TEXT1}</pre>'},
        {'tag_definition': '[hrcustom]', 'html_replacement': '<hr />', 'standalone': True},
        {'tag_definition': '[oo]{TEXT}', 'html_replacement': '<li>{TEXT}</li>', 'same_tag_closes': True},
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
        {'tag_definition': '[food]{CHOICE=apple,tomato,orange}[/food]', 'html_replacement': '<span>{CHOICE=apple,tomato,orange}</span>'},
        {'tag_definition': '[food++={CHOICE2=red,blue}]{CHOICE1=apple,tomato,orange}[/food++]', 'html_replacement': '<span data-choice="{CHOICE2=red,blue}">{CHOICE1=apple,tomato,orange}</span>'},
        {'tag_definition': '[big]{RANGE=2,15}[/big]', 'html_replacement': '<span>{RANGE=2,15}</span>'},
        {'tag_definition': '[b]{TEXT}[/b]', 'html_replacement': '<b>{TEXT}</b>'},  # Default tag overriding
    )

    def setup_method(self, method):
        self.parser = get_parser()

    def test_should_not_save_invalid_tags(self):
        # Run & check
        for tag_dict in self.ERRONEOUS_TAGS_TESTS:
            with pytest.raises(ValidationError):
                tag = BBCodeTag(**tag_dict)
                tag.clean()

    def test_should_save_valid_tags(self):
        # Run & check
        for tag_dict in self.VALID_TAG_TESTS:
            tag = BBCodeTag(**tag_dict)
            try:
                tag.clean()
            except ValidationError:
                self.fail('The following BBCode failed to validate: {}'.format(tag_dict))

    def test_should_allow_tag_updates_if_the_name_does_not_change(self):
        # Setup
        tag_dict = {'tag_definition': '[pr]{TEXT}[/pr]', 'html_replacement': '<pre>{TEXT}</pre>'}
        tag = BBCodeTag(**tag_dict)
        tag.save()
        # Run
        tag.html_replacement = '<span>{TEXT}</span>'
        # Check
        try:
            tag.clean()
        except ValidationError:
            self.fail('The following BBCode failed to validate: {}'.format(tag_dict))

    def test_should_allow_tag_creation_after_the_deletion_of_another_tag_with_the_same_name(self):
        # Setup
        tag_dict = {'tag_definition': '[pr]{TEXT}[/pr]', 'html_replacement': '<pre>{TEXT}</pre>'}
        tag = BBCodeTag(**tag_dict)
        tag.save()
        tag.delete()
        new_tag = BBCodeTag(**tag_dict)
        # Run & check
        try:
            new_tag.clean()
        except ValidationError:
            self.fail('The following BBCode failed to validate: {}'.format(tag_dict))

    def test_should_allow_tag_creation_after_the_bulk_deletion_of_another_tag_with_the_same_name_in_the_admin(self):
        # Setup
        tag_dict = {'tag_definition': '[pr2]{TEXT}[/pr2]', 'html_replacement': '<pre>{TEXT}</pre>'}
        tag = BBCodeTag(**tag_dict)
        tag.save()

        admin_user = User.objects.create_user('admin', 'admin@admin.io', 'adminpass')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        client = Client()
        client.login(username='admin', password='adminpass')
        url = reverse('admin:precise_bbcode_bbcodetag_changelist')
        r = client.post(url, data={
            'action': 'delete_selected', '_selected_action': [tag.pk, ], 'post': 'yes'})

        new_tag = BBCodeTag(**tag_dict)
        # Run & check
        try:
            new_tag.clean()
        except ValidationError:
            self.fail('The following BBCode failed to validate: {}'.format(tag_dict))

    def test_should_save_default_bbcode_tags_rewrites(self):
        # Setup
        tag = BBCodeTag(tag_definition='[b]{TEXT1}[/b]', html_replacement='<b>{TEXT1}</b>')
        # Run & check
        try:
            tag.clean()
        except ValidationError:
            self.fail('The following BBCode failed to validate: {}'.format(tag))

    def test_should_provide_the_required_parser_bbcode_tag_class(self):
        # Setup
        tag = BBCodeTag(**{'tag_definition': '[io]{TEXT}[/io]', 'html_replacement': '<b>{TEXT}</b>'})
        tag.save()
        # Run & check
        parser_tag_klass = tag.parser_tag_klass
        assert issubclass(parser_tag_klass, ParserBBCodeTag)
        assert parser_tag_klass.name == 'io'
        assert parser_tag_klass.definition_string == '[io]{TEXT}[/io]'
        assert parser_tag_klass.format_string == '<b>{TEXT}</b>'

    def test_can_be_rendered_by_the_bbcode_parser(self):
        # Setup
        parser_loader = BBCodeParserLoader(parser=self.parser)
        tag = BBCodeTag(**{'tag_definition': '[mail]{EMAIL}[/mail]',
                        'html_replacement': '<a href="mailto:{EMAIL}">{EMAIL}</a>', 'swallow_trailing_newline': True})
        tag.save()
        parser_loader.init_custom_bbcode_tags()
        # Run & check
        assert self.parser.render('[mail]xyz@xyz.com[/mail]') == '<a href="mailto:xyz@xyz.com">xyz@xyz.com</a>'
