from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser, Group as DjangoGroup
from django.utils.translation import gettext_lazy as _

class UsernameUnicodeValidator(validators.RegexValidator):
    regex = r'^(?!.*[_])(?!.*[.-]{2})(?![\d.-])[\w.-]{0,150}(?<![.-])$'
    message = _('Enter a valid username.')
    flags = 0

class Group(DjangoGroup):
    """
    Proxy model for Django's built-in Group model.

    This model ensures that the Group model appears in the same app as 
    the User model in the admin portal, as models are organized by apps 
    in Django. Consequently, It does not add any additional fields or 
    functionality to the original Group model.
    """

    class Meta:
        proxy = True

class User(AbstractUser):
    username_validator = UsernameUnicodeValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            "Your username must be at most 150 characters, and can only contain letters, "
            "numbers, hyphens, and periods. It can't begin with a number or a special character, "
            "end with a special character, or contain consecutive special characters."
        ),
        validators=[username_validator],
        error_messages={'unique': _('A user with that username already exists.')},
    )

    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    def get_short_name(self):
        return self.full_name

    def get_full_name(self):
        return self.full_name

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class OutstandingToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40) # SHA-1
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'auth_outstanding_token'
        verbose_name = _('Outstanding Token')
        verbose_name_plural = _('Outstanding Tokens')

    def __str__(self):
        return self.token
