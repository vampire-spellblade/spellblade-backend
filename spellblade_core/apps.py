from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class SpellbladeCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spellblade_core'
    verbose_name = _('Core')
