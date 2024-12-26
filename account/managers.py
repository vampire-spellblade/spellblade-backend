# pylint: disable=missing-module-docstring
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager): # pylint: disable=missing-class-docstring

    def create_user(self, email=None, password=None, **extra_fields):   # pylint: disable=missing-function-docstring
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):  # pylint: disable=missing-function-docstring
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
