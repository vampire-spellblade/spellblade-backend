from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

class User(AbstractUser):
    username = None
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    objects = UserManager()

    def __str__(self):
        return self.email

class Group(Group):

    class Meta:
        proxy = True
