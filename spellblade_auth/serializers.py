from hashlib import md5
from django.utils import timezone
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OutstandingToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    refresh_exp = serializers.DateTimeField(read_only=True)
    access = serializers.CharField(read_only=True)
    access_exp = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError(_('Invalid credentials'))

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        self.refresh_exp = timezone.datetime.fromtimestamp(refresh['exp'])
        self.access_exp = timezone.datetime.fromtimestamp(access['exp'])

        self.refresh = str(refresh)
        self.access = str(access)

        OutstandingToken.objects.create(
            user=user,
            token=md5(self.refresh.encode('utf-8')).hexdigest(),
            expires_at=self.refresh_exp
        )

        return self

class LoginRenewSerializer(serializers.Serializer):
    pass

class LogoutSerializer(serializers.Serializer):
    # Remove refresh token from OutstandingToken model.
    # User is not expected to be logged in at this point.
    pass

class LogoutAllSerializer(serializers.Serializer):
    # Remove all refresh tokens from OutstandingToken model associated with the user.
    # User is not expected to be logged in at this point.
    pass
