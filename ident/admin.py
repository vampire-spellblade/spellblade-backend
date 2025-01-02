# pylint: disable=missing-module-docstring
from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from .models import Group

admin.site.unregister(DjangoGroup)

@admin.site.register(Group)
class GroupAdmin(BaseGroupAdmin): # pylint: disable=missing-class-docstring
    pass
