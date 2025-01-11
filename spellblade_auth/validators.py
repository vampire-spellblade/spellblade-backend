from django.core import validators
from django.utils.translation import gettext_lazy as _

class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^(?!.*[_])(?!.*[.-]{2})(?![\d.-])[\w.-]{0,20}(?<![.-])$'
    message = _('Enter a valid username.')
    flags = 0
