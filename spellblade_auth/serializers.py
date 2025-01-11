from hashlib import sha1
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from spellblade.settings import SIMPLE_JWT
from .models import OutstandingToken

ROTATE_REFRESH_TOKENS = SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False)
UPDATE_LAST_LOGIN = SIMPLE_JWT.get('UPDATE_LAST_LOGIN', False)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    refresh = serializers.CharField(read_only=True)
    refresh_exp = serializers.DateTimeField(read_only=True)
    access = serializers.CharField(read_only=True)
    access_exp = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        self._user = authenticate(username=attrs['username'], password=attrs['password'])

        if not self._user:
            raise serializers.ValidationError(_('Invalid credentials'))

        return attrs

    def create(self, validated_data):
        refresh = RefreshToken.for_user(self._user)
        access = refresh.access_token

        self.refresh_exp = timezone.datetime.fromtimestamp(refresh['exp'])
        self.access_exp = timezone.datetime.fromtimestamp(access['exp'])

        self.refresh = str(refresh)
        self.access = str(access)

        OutstandingToken.objects.create(
            user=self._user,
            token=sha1(self.refresh.encode('utf-8')).hexdigest(),
            expires_at=self.refresh_exp
        )

        if UPDATE_LAST_LOGIN:
            update_last_login(None, self._user)

        return self

class LoginRenewSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    refresh = serializers.CharField(read_only=True, required=False)
    refresh_exp = serializers.DateTimeField(read_only=True, required=False)
    access = serializers.CharField(read_only=True)
    access_exp = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        try:
            self._refresh = RefreshToken(attrs['token'])
        except TokenError as e:
            raise serializers.ValidationError(e)

        try:
            self._token = OutstandingToken.objects.get(token=sha1(attrs['token'].encode('utf-8')).hexdigest())
        except OutstandingToken.DoesNotExist:
            raise serializers.ValidationError(_('Token is invalid.'))

        return attrs

    def create(self, validated_data):
        if ROTATE_REFRESH_TOKENS:
            self._refresh = RefreshToken.for_user(self._token.user)

            self.refresh_exp = timezone.datetime.fromtimestamp(self._refresh['exp'])
            self.refresh = str(self._refresh)

            self._token.token = sha1(self.refresh.encode('utf-8')).hexdigest()
            self._token.expires_at = self.refresh_exp
            self._token.save()

        access = self._refresh.access_token

        self.access_exp = timezone.datetime.fromtimestamp(access['exp'])
        self.access = str(access)

        return self

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            self._token = OutstandingToken.objects.get(token=sha1(attrs['token'].encode('utf-8')).hexdigest())
        except OutstandingToken.DoesNotExist:
            raise serializers.ValidationError(_('Token is invalid.'))

        return attrs

    def create(self, validated_data):
        self._token.delete()
        return self
