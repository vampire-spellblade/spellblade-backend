# pylint: disable=missing-module-docstring
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    Group as DjangoGroup,
    AbstractUser,
)

class Group(DjangoGroup):
    '''Proxy model for DjangoGroup.'''

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        proxy = True

class User(AbstractUser):
    '''User model tailored to allow email based authentication and more.'''
    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    def get_short_name(self):
        return self.full_name

    def get_full_name(self):
        return self.full_name
