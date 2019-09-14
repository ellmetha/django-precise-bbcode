# -*- coding: utf-8 -*-

import re


# Common regexes
url_re = re.compile(r'(?im)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\([^\s()<>]+\))+(?:\([^\s()<>]+\)|[^\s`!()\[\]{};:\'".,<>?]))')  # noqa


# BBCode placeholder regexes
placeholder_re = re.compile(r'{([a-zA-Z]+\d*=?[^\s\[\]\{\}=]*)}')
placeholder_content_re = re.compile(r'^(?P<placeholder_name>[a-zA-Z]+)(\d*)(=[^\s\[\]\{\}=]*)?$')


# BBCode regexes
#bbcodde_standard_re = r'^\[(?P<start_name>[^\s=\[\]]*)(=\{[a-zA-Z]+\d*=?[^\s\[\]\{\}=]*\})?\]\{[a-zA-Z]+\d*=?[^\s\[\]\{\}=]*\}(\[/(?P<end_name>[^\s=\[\]]*)\])?$'  # noqa
bbcodde_standard_re = r'^\[(?P<start_name>[^\s=\[\]]*)(=\{[a-zA-Z]+\d*=?[^\s\[\]\{\}=]*\})?(\s+(?P<named_types>\{(.*)\}=(.*)))*\]\{[a-zA-Z]+\d*=?[^\s\[\]\{\}=]*\}(\[/(?P<end_name>[^\s=\[\]]*)\])?$' # extended for named attributes
bbcodde_standalone_re = r'^\[(?P<start_name>[^\s=\[\]]*)(=\{[a-zA-Z]+\d*=?[^\s\[\]\{\}=]*\})?\]\{?[a-zA-Z]*\d*=?[^\s\[\]\{\}=]*\}?$'  # noqa
bbcode_content_re = re.compile(r'^\[[A-Za-z0-9]*\](?P<content>.*)\[/[A-Za-z0-9]*\]')
