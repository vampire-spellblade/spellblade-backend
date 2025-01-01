# pylint: disable=missing-module-docstring

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PasswordComplexityValidator: # pylint: disable=missing-class-docstring

    def validate(self, password, user=None): # pylint: disable=missing-function-docstring,unused-argument
        if any([
            not re.search(r'[A-Z]', password),
            not re.search(r'[a-z]', password),
            not re.search(r'[0-9]', password),
        ]):
            raise ValidationError(
                self.get_error_message(),
                code='password_too_simple',
            )

    def get_error_message(self):
        '''Returns the default error message'''
        return _('This password is too simple. It must contain at least one uppercase letter, one' +
                 ' lowercase letter, and one digit.')

    def get_help_text(self):
        '''Returns the default help text'''
        return _('Your password must contain at least one uppercase letter, one lowercase letter,' +
                 ' and one digit.')
