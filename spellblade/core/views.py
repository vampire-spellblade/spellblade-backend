from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from . import models
from . import serializers

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': token.key,
        }, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.user.is_authenticated:
        try:
            token = Token.objects.get(user=request.user)
            token.delete()

            return Response(status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            pass
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def signup(request):
    pass
