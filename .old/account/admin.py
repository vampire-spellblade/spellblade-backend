# pylint: disable=missing-module-docstring

from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
    GroupAdmin as BaseGroupAdmin,
)
from django.utils.translation import gettext_lazy as _
from .models import Group
from .forms import AdminUserCreationForm, UserChangeForm

# ========================================
# Group
# ========================================

admin.site.unregister(DjangoGroup)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin): # pylint: disable=missing-class-docstring
    pass

# ========================================
# User
# ========================================

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin): # pylint: disable=missing-class-docstring
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff',)
    search_fields = ('first_name', 'last_name', 'email',)

    add_form = AdminUserCreationForm
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

    form = UserChangeForm
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
