from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Group

admin.site.unregister(DjangoGroup)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'full_name', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'full_name')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'usable_password', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'email', 'full_name', 'password')}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'groups',
            'user_permissions',
        )}),
    )
