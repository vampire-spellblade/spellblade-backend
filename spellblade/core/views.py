from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from . import models
from . import serializers
from . import errors as core_errors

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    errors = []

    email = request.data.get('email')
    password = request.data.get('password')

    if not email:
        errors.append(core_errors.EMAIL_REQUIRED)
    elif not isinstance(email, str):
        errors.append(core_errors.EMAIL_TYPE_MISMATCH)
    else:
        email = email.strip().lower()

    if not password:
        errors.append(core_errors.PASSWORD_REQUIRED)
    elif not isinstance(password, str):
        errors.append(core_errors.PASSWORD_TYPE_MISMATCH)

    if len(errors) > 0:
        return Response({ 'errors': errors }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)

    if user is not None:
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        return Response({
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'access_token': access_token,
            'refresh_token': str(refresh_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({ 'errors': [core_errors.INVALID_CREDENTIALS] }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({ 'errors': [core_errors.REFRESH_TOKEN_REQUIRED] }, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh_token = RefreshToken(refresh_token)
    except TokenError:
        return Response({ 'errors': [core_errors.INVALID_REFRESH_TOKEN] }, status=status.HTTP_400_BAD_REQUEST)

    if refresh_token['user_id'] != request.user.id:
        return Response({ 'errors': [core_errors.INVALID_REFRESH_TOKEN] }, status=status.HTTP_400_BAD_REQUEST)

    refresh_token.blacklist()

    return Response(status=status.HTTP_200_OK)

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
        errors.append(core_errors.FIRST_NAME_REQUIRED)
    elif not isinstance(first_name, str):
        errors.append(core_errors.FIRST_NAME_TYPE_MISMATCH)
    else:
        first_name = first_name.strip()

        if len(first_name) > 64:
            errors.append(core_errors.FIRST_NAME_LENGTH_MISMATCH)

    if not last_name:
        errors.append(core_errors.LAST_NAME_REQUIRED)
    elif not isinstance(last_name, str):
        errors.append(core_errors.LAST_NAME_TYPE_MISMATCH)
    else:
        last_name = last_name.strip()

        if len(last_name) > 64:
            errors.append(core_errors.LAST_NAME_LENGTH_MISMATCH)

    if not email:
        errors.append(core_errors.EMAIL_REQUIRED)
    elif not isinstance(email, str):
        errors.append(core_errors.EMAIL_TYPE_MISMATCH)
    else:
        email = email.strip().lower()

        validate_email = EmailValidator()

        if len(email) > 192:
            errors.append(core_errors.EMAIL_LENGTH_MISMATCH)
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append(core_errors.INVALID_EMAIL_FORMAT)

    if not password:
        errors.append(core_errors.PASSWORD_REQUIRED)
    elif not isinstance(password, str):
        errors.append(core_errors.PASSWORD_TYPE_MISMATCH)
    else:
        try:
            validate_password(password)
        except ValidationError:
            errors.append(core_errors.PASSWORD_TOO_WEAK)

    if models.User.objects.filter(email=email).exists():
        errors.append(core_errors.ACCOUNT_ALREADY_EXISTS)

    if len(errors) > 0:
        return Response({ 'errors': errors }, status=status.HTTP_400_BAD_REQUEST)

    serializer = serializers.UserSerializer(data={
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
    })

    if serializer.is_valid():
        user = serializer.save()

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        return Response({
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'access_token': access_token,
            'refresh_token': str(refresh_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({ 'errors': [core_errors.UNEXPECTED_ERROR] }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_renew(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({ 'errors': [core_errors.REFRESH_TOKEN_REQUIRED] }, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh_token = RefreshToken(refresh_token)
    except TokenError:
        return Response({ 'errors': [core_errors.INVALID_REFRESH_TOKEN] }, status=status.HTTP_400_BAD_REQUEST)

    if refresh_token['user_id'] != request.user.id:
        return Response({ 'errors': [core_errors.INVALID_REFRESH_TOKEN] }, status=status.HTTP_400_BAD_REQUEST)

    access_token = str(refresh_token.access_token)
    return Response({ 'access_token': access_token }, status=status.HTTP_200_OK)
