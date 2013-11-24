# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals

# Third party imports
from django.db import models
from django.db.models import signals

# Local application / specific library imports
from .parser import get_parser


_rendered_content_field_name = lambda name: '{}_rendered'.format(name)


class BBCodeContent(object):
    def __init__(self, raw, rendered=None):
        self.raw = raw
        self.rendered = rendered

    def __unicode__(self):
        return '{}'.format(self.raw)


class BBCodeTextCreator(object):
    """
    Acts as the Django's default attribute descriptor class (enabled via the SubfieldBase metaclass).
    The main difference is that it does not call to_python() on the BCodeTextField class. Instead, it
    stores the two different values of a BBCode content (the raw and the rendered data) separately.
    These values can be separately updated when something is assigned. When the field is accessed,
    a BBCodeContent instance will be returned ; this one is built with the current data.
    """
    def __init__(self, field):
        self.field = field
        self.rendered_field_name = _rendered_content_field_name(self.field.name)

    def __get__(self, instance, type=None):
        if instance is None:
            return self.field
        raw_content = instance.__dict__[self.field.name]
        if raw_content is None:
            return None
        else:
            return BBCodeContent(raw_content, rendered=getattr(instance, self.rendered_field_name))

    def __set__(self, instance, value):
        if isinstance(value, BBCodeContent):
            instance.__dict__[self.field.name] = value.raw
            setattr(instance, self.rendered_field_name, value.rendered)
        else:
            # Set only the bbcode content field
            instance.__dict__[self.field.name] = self.field.to_python(value)


class BBCodeTextField(models.TextField):
    """
    A BBCode text field contributes two columns to the model instead of the standard single column.
    The initial column stores the BBCode content and the other one keeps the rendered content returned
    by the BBCode parser.
    """
    def contribute_to_class(self, cls, name):
        self.raw_name = name
        self.rendered_field_name = _rendered_content_field_name(name)

        # Create a hidden 'rendered' field
        rendered = models.TextField(editable=False, null=True, blank=True)
        # Ensure that the 'rendered' field appears before the actual field in
        # the models _meta.fields
        rendered.creation_counter = self.creation_counter
        cls.add_to_class(self.rendered_field_name, rendered)

        # The data will be processed before each save
        signals.pre_save.connect(self.process_bbcodes, sender=cls)

        # Add the default text field
        super(BBCodeTextField, self).contribute_to_class(cls, name)

        self.set_descriptor_class(cls)

    def set_descriptor_class(self, cls):
        setattr(cls, self.name, BBCodeTextCreator(self))

    def get_db_prep_save(self, value, connection):
        if isinstance(value, BBCodeContent):
            value = value.raw
        return super(BBCodeTextField, self).get_db_prep_save(value, connection)

    def process_bbcodes(self, signal, sender, instance=None, **kwargs):
        bbcode_text = getattr(instance, self.raw_name)

        if isinstance(bbcode_text, BBCodeContent):
            bbcode_text = bbcode_text.raw

        rendered = ''
        if bbcode_text:
            parser = get_parser()
            rendered = parser.render(bbcode_text)

        setattr(instance, self.rendered_field_name, rendered)

    def south_field_triple(self):
        """
        Returns a suitable description of this field for South.
        """
        try:
            from south.modelsinspector import introspector
            cls_name = '{0}.{1}'.format(
                self.__class__.__module__,
                self.__class__.__name__)
            args, kwargs = introspector(self)
            return cls_name, args, kwargs
        except ImportError:
            pass
