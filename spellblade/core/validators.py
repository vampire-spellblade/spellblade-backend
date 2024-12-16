from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

class PasswordComplexityValidator:

    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('The password must contain at least one uppercase letter.'))

        if not re.search(r'[a-z]', password):
            raise ValidationError(_('The password must contain at least one lowercase letter.'))

        if not re.search(r'\d', password):
            raise ValidationError(_('The password must contain at least one number.'))

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_('The password must contain at least one special character.'))

    def get_help_text(self):
        return _("The password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
