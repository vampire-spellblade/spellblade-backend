# pylint: disable=missing-module-docstring

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from .serializers import (
    UserCreationSerializer,
    UserChangePersonalInfoSerializer,
    UserChangeEmailSerializer,
    UserChangePasswordSerializer,
)

class LoginView(TokenObtainPairView):
    '''View for user login'''

class LoginRenewView(TokenRefreshView):
    '''View for user login renew'''

class LoginVerifyView(TokenVerifyView):
    '''View for user login verify'''

class LogoutView(TokenBlacklistView):
    '''View for user logout'''

class SignUpView(APIView):
    '''View for signing up a new user'''
    permission_classes = []

    serializer_class = UserCreationSerializer

    def get_serializer(self): # pylint: disable=missing-function-docstring
        return self.serializer_class()

    def post(self, request):
        '''POST requests handling logic'''
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePersonalInfoView(APIView):
    '''View for updating user personal info'''
    serializer_class = UserChangePersonalInfoSerializer

    def get_serializer(self): # pylint: disable=missing-function-docstring
        return self.serializer_class()

    def put(self, request):
        '''PUT requests handling logic'''
        serializer = self.serializer_class(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateEmailView(APIView):
    '''View for updating user email'''
    serializer_class = UserChangeEmailSerializer

    def get_serializer(self): # pylint: disable=missing-function-docstring
        return self.serializer_class()

    def put(self, request):
        '''PUT requests handling logic'''
        serializer = self.serializer_class(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(APIView):
    '''View for updating user password'''
    serializer_class = UserChangePasswordSerializer

    def get_serializer(self): # pylint: disable=missing-function-docstring
        return self.serializer_class()

    def put(self, request):
        '''PUT requests handling logic'''
        serializer = self.serializer_class(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
