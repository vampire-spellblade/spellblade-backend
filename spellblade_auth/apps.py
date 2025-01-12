from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class SpellbladeAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spellblade_auth'
    verbose_name = _('Authentication & Authorization')
