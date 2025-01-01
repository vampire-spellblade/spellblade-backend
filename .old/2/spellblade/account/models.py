from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Email(models.Model):
    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return self.email

class User(AbstractUser):
    # I'm removing first_name and last_name fields, and instead adding full_name field.
    # Just like the other two, it's optional and based on the fact that the same is used
    # by Medium and Reddit.
    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), blank=True)

    email = models.ForeignKey(Email, on_delete=models.CASCADE)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name
