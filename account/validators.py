import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PasswordComplexityValidator:

    def validate(self, password, user=None) -> None:
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'`~!@#$%^&*()?\'",.:;<>/{}|[]', password):
            raise ValidationError(_('This password is too simple. It must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.'))

    def get_help_text(self) -> str:
        return _('Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
