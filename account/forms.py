# pylint: disable=missing-module-docstring
from django.contrib.auth.forms import AdminUserCreationForm as BaseAdminUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import User

class AdminUserCreationForm(BaseAdminUserCreationForm): # pylint: disable=missing-class-docstring,too-many-ancestors

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = User
        fields = ('email', 'first_name', 'last_name',)
        field_classes = {}

class UserChangeForm(BaseUserChangeForm):   # pylint: disable=missing-class-docstring

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = User
        fields = ('email',)
        field_classes = {}
