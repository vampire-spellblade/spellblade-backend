# pylint: disable=missing-module-docstring
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.utils.translation import gettext_lazy as _
from . import models
from . import forms

admin.site.unregister(Group)

@admin.register(models.Group)
class GroupAdmin(BaseGroupAdmin):   # pylint: disable=missing-class-docstring
    pass

@admin.register(models.User)
class UserAdmin(BaseUserAdmin): # pylint: disable=missing-class-docstring
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff',)
    search_fields = ('first_name', 'last_name', 'email',)

    add_form = forms.AdminUserCreationForm
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'usable_password',
                    'password1',
                    'password2',
                ),
            },
        ),
    )

    form = forms.UserChangeForm
    fieldsets = (
        (
            None, {
                'fields': ('email', 'password',),
            },
        ),
        (
            _('Personal info'),
            {
                'fields': ('first_name', 'last_name',),
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
    )
