from importlib import import_module
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from spellblade.settings import AUTH_PASSWORD_VALIDATORS

User = get_user_model()

class SignUpView(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(31536000))
    def get(self, request):
        username_field = User._meta.get_field(User.USERNAME_FIELD)
        response = {
            'username': [username_field.help_text],
            'password': [],
        }

        for validator in AUTH_PASSWORD_VALIDATORS:
            try:
                validator_class_path = validator['NAME']
                module_path, class_name = validator_class_path.rsplit('.', 1)
                module = import_module(module_path)
                validator_class = getattr(module, class_name)

                response['password'].append(validator_class().get_help_text())
            except:
                pass

        return Response(response, status=status.HTTP_200_OK)
