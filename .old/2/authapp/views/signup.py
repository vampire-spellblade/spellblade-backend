from importlib import import_module
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from spellblade.settings import AUTH_PASSWORD_VALIDATORS
from ..serializers.create_user import UserCreationSerializer
from ..models import User

class SignUpView(APIView):
    '''Registers a new user.'''
    permission_classes = (AllowAny,)
    serializer_class = UserCreationSerializer

    def get_serializer(self):
        return self.serializer_class()

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

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
