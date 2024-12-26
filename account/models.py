# pylint: disable=missing-module-docstring

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    Group as DjangoGroup,
)
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

class User(AbstractUser):
    '''
    User model tailored to use email instead of username,
    and enforce use of first and last name fields.
    '''
    username = None
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

class Group(DjangoGroup):
    '''Proxy model for DjangoGroup'''

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        proxy = True
