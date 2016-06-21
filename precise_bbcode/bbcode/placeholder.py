# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re

from precise_bbcode.bbcode.exceptions import InvalidBBCodePlaholder
from precise_bbcode.core.compat import with_metaclass


class BBCodePlaceholderBase(type):
    """
    Metaclass for all BBCode placehplders.
    This metaclass ensure that the BBCode placeholders subclasses have the required values
    and proceed to some validations.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(BBCodePlaceholderBase, cls).__new__
        parents = [base for base in bases if isinstance(base, BBCodePlaceholderBase)]

        if not parents:
            # Stop here if we are considering the top-level class to which the
            # current metaclass was applied and not one of its subclasses.
            # eg. BBCodeTag
            return super_new(cls, name, bases, attrs)

        # Construct the BBCode placeholder class
        new_placeholder = super_new(cls, name, bases, attrs)

        # Validates the placeholder name
        if not hasattr(new_placeholder, 'name'):
            raise InvalidBBCodePlaholder(
                'BBCodePlaceholderBase subclasses must have a \'name\' attribute'
            )
        if not new_placeholder.name:
            raise InvalidBBCodePlaholder(
                'The \'name\' attribute associated with InvalidBBCodePlaholder subclasses '
                'cannot be None'
            )
        if not re.match('^[\w]+$', new_placeholder.name):
            raise InvalidBBCodePlaholder(
                """The \'name\' attribute associated with {!r} is not valid: a placeholder name must be strictly
                composed of alphanumeric character""".format(name)
            )

        # Validates the placeholder pattern if present
        if new_placeholder.pattern and not isinstance(new_placeholder.pattern, re._pattern_type):
            raise InvalidBBCodePlaholder(
                """The \'pattern\' attribute associated with {!r} is not valid: a placeholder pattern must be an
                instance of a valid regex type""".format(name)
            )

        return new_placeholder


class BBCodePlaceholder(with_metaclass(BBCodePlaceholderBase)):
    name = None
    pattern = None

    def validate(self, content, extra_context=None):
        """
        The validate function is used to check whether the given content is valid
        according to the placeholder definition associated to it.

            content
                The content used to fill the placeholder that must be validated.
            extra_context
                The extra context of the placeholder if defined in a tag definition.

        Note that the extra context of a placeholder always corresponds to the string
        positioned after the '='' sign in the definition of the placeholder in the
        considered BBCode tag.
        For example, consider the following placeholder definition:

            {TEXT1=4,3}

        'TEXT' is the name of the placeholder while '4,3' is the extra context of the
        placeholder. This extra context could be used to perform extra validation.

        The default implementation of the 'validate' method will use the regex pattern
        provided by the 'pattern' attribute to validate any passed content. Note that this
        default behavior can be updated with another logic by overriding this method.
        """
        if self.pattern:
            # This is the default case: validates the passed content by using a
            # specified regex pattern.
            return re.search(self.pattern, content)

        # In any other case a NotImplementedError is raised to ensure
        # that any subclasses must override this method
        raise NotImplementedError
