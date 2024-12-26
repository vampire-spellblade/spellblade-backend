# pylint: disable=missing-module-docstring

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AccountConfig(AppConfig): # pylint: disable=missing-class-docstring
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    verbose_name = _('Authentication and Authorization')
