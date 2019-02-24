from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.tag_pool import tag_pool


class LoadDummyTag(BBCodeTag):
    name = 'loaddummy02'
    definition_string = '[loaddummy02]{TEXT}[/loaddummy02]'
    format_string = '<loaddummy>{TEXT}</loaddummy>'


tag_pool.register_tag(LoadDummyTag)
