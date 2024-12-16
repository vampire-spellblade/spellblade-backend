from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.translation import gettext_lazy as _
from . import models
from . import serializers

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    errors = []

    email = request.data.get('email')
    password = request.data.get('password')

    if not email:
        errors.append(_('Email required'))
    elif not isinstance(email, str):
        errors.append(_('Email must be a string'))
    else:
        email = email.strip().lower()

    if not password:
        errors.append(_('Password required'))
    elif not isinstance(password, str):
        errors.append(_('Password must be a string'))

    if len(errors) > 0:
        return Response({ 'error': errors }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)

    if user is not None:
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        return Response({
            'message': _('Login successful'),
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'access_token': access_token,
                'refresh_token': str(refresh_token),
            },
        }, status=status.HTTP_200_OK)
    else:
        return Response({ 'error': [_('Incorrect email or password')] }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({ 'error': [_('Refresh token required')] }, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh_token = RefreshToken(refresh_token)
    except TokenError:
        return Response({ 'error': [_('Invalid refresh token')] }, status=status.HTTP_400_BAD_REQUEST)

    if refresh_token['user_id'] != request.user.id:
        return Response({ 'error': [_('Invalid refresh token')] }, status=status.HTTP_400_BAD_REQUEST)

    refresh_token.blacklist()

    return Response({ 'message': _('Logout successful') }, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def sign_up(request):
    errors = []

    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    if not first_name:
        errors.append(_('First name required'))
    elif not isinstance(first_name, str):
        errors.append(_('First name must be a string'))
    else:
        first_name = first_name.strip()

        if len(first_name) < 2 or len(first_name) > 64:
            errors.append(_('First name must be between 2 and 64 characters'))

    if not last_name:
        errors.append(_('Last name required'))
    elif not isinstance(last_name, str):
        errors.append(_('Last name must be a string'))
    else:
        last_name = last_name.strip()

        if len(last_name) < 2 or len(last_name) > 64:
            errors.append(_('Last name must be between 2 and 64 characters'))

    if not email:
        errors.append(_('Email required'))
    elif not isinstance(email, str):
        errors.append(_('Email must be a string'))
    else:
        email = email.strip().lower()

        validate_email = EmailValidator()

        if len(email) < 3 or len(email) > 192:
            errors.append(_('Email must be between 3 and 192 characters'))
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append(_('Email is invalid'))

    if not password:
        errors.append(_('Password required'))
    elif not isinstance(password, str):
        errors.append(_('Password must be a string'))
    else:
        try:
            validate_password(password)
        except ValidationError:
            errors.append(_('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character'))

    if models.User.objects.filter(email=email).exists():
        errors.append(_('Account already exists'))

    if len(errors) > 0:
        return Response({ 'error': errors }, status=status.HTTP_400_BAD_REQUEST)

    serializer = serializers.UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        return Response({
            'message': _('Signup successful'),
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'access_token': access_token,
                'refresh_token': str(refresh_token),
            },
        }, status=status.HTTP_200_OK)
    else:
        return Response({ 'error': _('Invalid data') }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_renew(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({ 'error': [_('Refresh token required')] }, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh_token = RefreshToken(refresh_token)
    except TokenError:
        return Response({ 'error': [_('Invalid refresh token')] }, status=status.HTTP_400_BAD_REQUEST)

    if refresh_token['user_id'] != request.user.id:
        return Response({ 'error': [_('Invalid refresh token')] }, status=status.HTTP_400_BAD_REQUEST)

    access_token = str(refresh_token.access_token)
    return Response({ 'user': { 'access_token': access_token } }, status=status.HTTP_200_OK)
