from django.contrib.auth.models import UserManager as BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        first_name = extra_fields.pop('first_name').strip()
        last_name = extra_fields.pop('last_name').strip()
        is_superuser = extra_fields.get('is_superuser', False)

        if (not first_name or len(first_name) < 2 or len(first_name) > 64) and not is_superuser:
            raise ValueError(_('The first name must be between 2 and 64 characters.'))

        if (not last_name or len(last_name) < 2 or len(last_name) > 64) and not is_superuser:
            raise ValueError(_('The last name must be between 2 and 64 characters.'))

        if (not email or len(email) < 3 or len(email) > 192) and not is_superuser:
            raise ValueError(_('The email must be between 3 and 192 characters.'))

        if (not password or len(password) < 8) and not is_superuser:
            raise ValueError(_('The password must be at least 8 characters long.'))

        email = self.normalize_email(email.strip().lower())
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)
