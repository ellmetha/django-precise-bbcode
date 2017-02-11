# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest

from precise_bbcode.core.loading import load
from precise_bbcode.tag_pool import tag_pool


@pytest.mark.django_db
class TestLoadFunction(object):
    def test_can_load_modules_from_classic_apps(self):
        # Setup
        load('dummymodule01')
        assert 'loaddummy01' in tag_pool.tags

    def test_can_load_modules_from_appconfig_classes(self):
        # Setup
        load('dummymodule02')
        assert 'loaddummy02' in tag_pool.tags
