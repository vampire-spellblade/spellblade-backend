from django.core import validators
from django.utils.translation import gettext_lazy as _

class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^(?!.*[_])(?!.*[.-]{2})(?![\d.-])[\w.-]{0,20}(?<![.-])$'
    message = _(
        'Enter a valid username. This value must be between 1 and 20 characters long, and '
        'can only contain letters, numbers, hyphens, and periods. It also can\'t start with a '
        'number or a special character, end with a special character, or contain consecutive '
        'special characters.'
    )
    flags = 0
