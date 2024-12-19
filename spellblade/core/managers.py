from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_superuser', False):
            validate_password(password)

        user = self.model(
            email=self.normalize_email(email.strip().lower()),
            first_name=extra_fields.pop('first_name').strip(),
            last_name=extra_fields.pop('last_name').strip(),
            **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
