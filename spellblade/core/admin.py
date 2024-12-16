from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from . import models
from . import forms

admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)

@admin.register(models.User)
class Users(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'last_login',)
    search_fields = ('email', 'first_name', 'last_name',)

    add_form = forms.UserCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2',)
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name',)
        }),
        ('Groups and Permissions', {
            'fields': ('groups', 'user_permissions', 'is_active', 'is_staff',)
        }),
    )

    form = forms.UserChangeForm
    fieldsets = (
        (None, {
            'fields': ('email', 'password',)
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name',)
        }),
        ('Groups and Permissions', {
            'fields': ('groups', 'user_permissions', 'is_active', 'is_staff',)
        }),
    )
