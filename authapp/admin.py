from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import (
    GroupAdmin,
    UserAdmin as BaseUserAdmin,
)
from .models import Group, User

admin.site.unregister(DjangoGroup)
admin.site.register(Group, GroupAdmin)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    '''Admin dashboard for User model.'''
    list_display = ('username', 'email', 'full_name', 'is_staff',)
    list_filter = ('is_staff', 'is_active', 'groups',)
    search_fields = ('username', 'email', 'full_name',)

    add_fieldsets = ((None, {
        'classes': ('wide'),
        'fields': ('email', 'username', 'usable_password', 'password1', 'password2'),
    }))

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'groups',
            'user_permissions',
        )}),
    )
