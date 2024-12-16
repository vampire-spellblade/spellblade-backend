from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . import models

class UserCreationForm(UserCreationForm):

    class Meta:
        model = models.User
        fields = ('email',)

class UserChangeForm(UserChangeForm):

    class Meta:
        model = models.User
        fields = ('email',)
