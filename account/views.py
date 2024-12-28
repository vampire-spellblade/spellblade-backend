# pylint: disable=missing-module-docstring

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserCreationSerializer,
    UserChangePersonalInfoSerializer,
    UserChangeEmailSerializer,
    UserChangePasswordSerializer,
)

class SignUpView(APIView):
    '''View for signing up a new user'''

    def post(self, request):
        '''POST requests handling logic'''
        serializer = UserCreationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePersonalInfoView(APIView):
    '''View for updating user personal info'''

    def put(self, request):
        '''PUT requests handling logic'''
        serializer = UserChangePersonalInfoSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateEmailView(APIView):
    '''View for updating user email'''

    def put(self, request):
        '''PUT requests handling logic'''
        serializer = UserChangeEmailSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(APIView):
    '''View for updating user password'''

    def put(self, request):
        '''PUT requests handling logic'''
        serializer = UserChangePasswordSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
