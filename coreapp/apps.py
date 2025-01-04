# pylint: disable=missing-module-docstring
from django.apps import AppConfig

class CoreAppConfig(AppConfig): # pylint: disable=missing-class-docstring
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coreapp'
    verbose_name = 'core'
