from django.contrib.auth.backends import ModelBackend as BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class ModelBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(User.EMAIL_FIELD)
        if email is None or password is None:
            return None

        try:
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            User().set_password(password)
        else:
            return user if user.check_password(password) and self.user_can_authenticate(user) else None
