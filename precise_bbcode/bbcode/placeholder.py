# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import re

# Third party imports
# Local application / specific library imports


class BBCodePlaceholder(object):
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

        # In any other case a NotImplementedError is raised to ensure
        # that any subclasses must override this method
        raise NotImplementedError
