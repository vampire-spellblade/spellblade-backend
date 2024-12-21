from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .forms import UserCreationForm, UserChangeForm
from . import models

admin.site.unregister(Group)

@admin.register(models.Group)
class Groups(GroupAdmin):
    pass

@admin.register(models.User)
class Users(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'last_login',)
    search_fields = ('email', 'first_name', 'last_name',)

    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2',)
        }),
    )

    form = UserChangeForm
    fieldsets = (
        (None, {
            'fields': ('email', 'password',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'groups', 'user_permissions',)
        }),
    )
