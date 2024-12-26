# pylint: disable=missing-module-docstring

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    '''Manager for user model'''

    def create_user(self, email=None, password=None, **extra_fields):
        '''Creates a new user'''
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        '''Creates a new superuser'''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
