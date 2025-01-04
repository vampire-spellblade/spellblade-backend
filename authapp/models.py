from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    Group as DjangoGroup,
    AbstractUser,
)
from spellblade.settings import SIMPLE_JWT

class Group(DjangoGroup):

    class Meta:
        proxy = True

class User(AbstractUser):
    # TODO: Update unicode validator for username. (Priority: High)
    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    class Meta:
        db_table = 'auth_user'

    def get_short_name(self):
        return self.full_name

    def get_full_name(self):
        return self.full_name

class OutstandingToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
    expires_at = models.DateTimeField(
        default = now() + SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
    )

    class Meta:
        db_table = 'auth_outstanding_token'

    def __str__(self):
        return self.token
