# pylint: disable=missing-module-docstring
from django.contrib.auth.backends import ModelBackend as BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class ModelBackend(BaseBackend):
    '''
    Authenticates user with email instead of username.
    Aimed to be used alongside the original auth backend to allow login either username or email.
    '''

    def authenticate(self, request, email=None, password=None, **kwargs): # pylint: disable=arguments-renamed,inconsistent-return-statements
        if email is None:
            email = kwargs.get(User.EMAIL_FIELD)
        if email is None or password is None:
            return
        try:
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
