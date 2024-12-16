from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from . import models
from . import serializers

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user is not None:
        token = Token.objects.create(user=user)

        return Response({
            'message': _('Login successful'),
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': token.key,
            },
        }, status=status.HTTP_200_OK)
    else:
        return Response({ 'error': _('Invalid email or password') }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    token = request.auth
    token.delete()

    return Response({ 'message': _('Logout successful') }, status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    if not first_name or len(first_name) == 0:
        return Response({ 'error': _('The first name is required.') }, status=status.HTTP_400_BAD_REQUEST)

    if not last_name or len(last_name) == 0:
        return Response({ 'error': _('The last name is required.') }, status=status.HTTP_400_BAD_REQUEST)

    if not password or len(password) == 0:
        return Response({ 'error': _('The password is required.') }, status=status.HTTP_400_BAD_REQUEST)

    if models.User.objects.filter(email=email).exists():
        return Response({ 'error': _('The account already exists.') }, status=status.HTTP_409_CONFLICT)

    serializer = serializers.UserSerializer(data=request.data)

    if serializer.is_valid():
        try:
            user = serializer.save()
        except ValueError as e:
            return Response({ 'error': _(f'{e}') }, status=status.HTTP_400_BAD_REQUEST)

        token = Token.objects.get_or_create(user=user)

        return Response({
            'message': _('Signup successful'),
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': token.key,
            },
        }, status=status.HTTP_200_OK)
    else:
        return Response({ 'error': _('The email is not valid.') }, status=status.HTTP_400_BAD_REQUEST)
