# pylint: disable=missing-module-docstring
from django.apps import AppConfig

class IdentConfig(AppConfig): # pylint: disable=missing-class-docstring
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    verbose_name = 'Authentication & Authorization'
