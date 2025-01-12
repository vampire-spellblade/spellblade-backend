from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import (
    GroupAdmin as BaseGroupAdmin,
    UserAdmin as BaseUserAdmin,
)
from django.utils.translation import gettext_lazy as _
from .models import Group, User, OutstandingToken

admin.site.unregister(DjangoGroup)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'full_name', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'full_name')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'usable_password', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'groups',
            'user_permissions',
        )}),
    )

@admin.register(OutstandingToken)
class OutstandingTokenAdmin(admin.ModelAdmin):
    ordering = ('user', 'expires_at')
    list_display = ('user', 'email', 'full_name', 'token', 'expires_at')
    search_fields = ('user__username', 'user__email', 'user__full_name', 'token')

    actions = None

    def get_readonly_fields(self, *args, **kwargs):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, request, obj=None):
        return request.method in ["GET", "HEAD"] and super().has_change_permission(request, obj)

    def email(self, obj):
        return obj.user.email

    def full_name(self, obj):
        return obj.user.full_name
