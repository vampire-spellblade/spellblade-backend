# pylint: disable=missing-module-docstring
from django.apps import AppConfig

class AuthAppConfig(AppConfig): # pylint: disable=missing-class-docstring
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'
    verbose_name = 'authentication & authorization'
