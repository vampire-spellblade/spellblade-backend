from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from .models import User

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class AdminPasswordChangeForm(AdminPasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'usable_password' in self.fields:
            del self.fields['usable_password']
