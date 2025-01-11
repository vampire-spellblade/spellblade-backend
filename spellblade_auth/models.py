from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group as DjangoGroup

class Group(DjangoGroup):

    class Meta:
        proxy = True

class User(AbstractUser):
    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name
