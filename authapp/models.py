# pylint: disable=missing-module-docstring
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    Group as DjangoGroup,
    AbstractUser,
)
from spellblade.settings import SIMPLE_JWT

class Group(DjangoGroup):
    '''Proxy model for DjangoGroup.'''

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        proxy = True

class User(AbstractUser):
    '''User model tailored to allow email based authentication and more.'''
    # TODO: update unicode validator for username
    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        db_table = 'auth_user'

    def get_short_name(self):
        return self.full_name

    def get_full_name(self):
        return self.full_name

class OutstandingToken(models.Model):
    '''Outstanding tokens model to serve as a whitelist.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
    expires_at = models.DateTimeField(
        default = now() + SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
    )

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        db_table = 'auth_outstanding_token'

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.token
