# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import unicode_literals
import re

# Third party imports
# Local application / specific library imports


class BaseBBCodePlaceholder(object):
    name = None
    pattern = None

    def validate(self, content):
        """
        The validate function is used check whether the given content is valid
        according to the placeholder definition associated to it.

            content
                The content used to fill the placeholder that must be validated.

        The default implementation will use the regex pattern provided by the 'pattern'
        attribute to validate any passed content. Note that this default behavior can
        be updated with another logic by overriding the 'validate' method.
        """
        if self.pattern:
            # This is the default case: validates the passed content by using a
            # specified regex pattern.
            return re.search(self.pattern, content)

        # In any other case a NotImplementedError is raised to ensure
        # that any subclasses must override this method
        raise NotImplementedError
