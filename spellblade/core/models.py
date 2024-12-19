from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from . import managers

class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=64)
    last_name = models.CharField(_('last name'), max_length=64)
    username = None
    email = models.EmailField(_('email address'), max_length=192, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = managers.UserManager()

    def __str__(self):
        return self.email
