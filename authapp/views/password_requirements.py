from importlib import import_module
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from spellblade.settings import AUTH_PASSWORD_VALIDATORS

class PasswordRequirementsView(APIView):
    '''Provides the password requirements for the user registration process.'''
    permission_classes = (AllowAny,)

    def get(self, request):
        response = {'password_requirements': []}

        for validator in AUTH_PASSWORD_VALIDATORS:
            try:
                validator_class_path = validator['NAME']
                module_path, class_name = validator_class_path.rsplit('.', 1)
                module = import_module(module_path)
                validator_class = getattr(module, class_name)

                response['password_requirements'].append(validator_class().get_help_text())
            except:
                pass

        return Response(response, status=status.HTTP_200_OK)
