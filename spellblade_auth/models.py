from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group as DjangoGroup
from .validators import UnicodeUsernameValidator

class Group(DjangoGroup):

    class Meta:
        proxy = True

class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        help_text=_(
            'Your username must be between 1 and 20 characters, and can only contain letters, '
            'numbers, hyphens, and periods. It also can\'t start with a number or a special '
            'character, end with a special character, or contain consecutive special characters.'
        ),
        validators=[username_validator],
        error_messages={'unique': _('A user with that username already exists.'),},
    )

    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name
