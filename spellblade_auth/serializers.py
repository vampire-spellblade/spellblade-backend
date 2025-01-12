from hashlib import sha1
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import OutstandingToken

UPDATE_LAST_LOGIN = settings.SIMPLE_JWT.get('UPDATE_LAST_LOGIN', False)
ROTATE_REFRESH_TOKENS = settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    refresh = serializers.CharField(read_only=True)
    refresh_exp = serializers.DateTimeField(read_only=True)
    access = serializers.CharField(read_only=True)
    access_exp = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        self.user = authenticate(username=attrs['username'], password=attrs['password'])

        if not self.user:
            raise serializers.ValidationError(_('Invalid credentials'))

        return attrs

    def create(self, validated_data):
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token

        self.refresh_exp = timezone.make_aware(timezone.datetime.fromtimestamp(refresh['exp']))
        self.access_exp = timezone.make_aware(timezone.datetime.fromtimestamp(access['exp']))

        self.refresh = str(refresh)
        self.access = str(access)

        OutstandingToken.objects.create(
            user=self.user,
            token=sha1(self.refresh.encode('utf-8')).hexdigest(),
            expires_at=self.refresh_exp
        )

        if UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return self

class LoginRenewSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    refresh = serializers.CharField(read_only=True, required=False)
    refresh_exp = serializers.DateTimeField(read_only=True, required=False)
    access = serializers.CharField(read_only=True)
    access_exp = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        try:
            self.token_obj = RefreshToken(attrs['token'])
        except TokenError as e:
            raise serializers.ValidationError(e)

        try:
            self.outstanding_token = OutstandingToken.objects.get(token=sha1(attrs['token'].encode('utf-8')).hexdigest())
        except OutstandingToken.DoesNotExist:
            raise serializers.ValidationError(_('Token is invalid.'))

        return attrs

    def create(self, validated_data):
        if ROTATE_REFRESH_TOKENS:
            self.token_obj = RefreshToken.for_user(self.outstanding_token.user)

            self.refresh_exp = timezone.make_aware(timezone.datetime.fromtimestamp(self.token_obj['exp']))
            self.refresh = str(self.token_obj)

            self.outstanding_token.token = sha1(self.refresh.encode('utf-8')).hexdigest()
            self.outstanding_token.expires_at = self.refresh_exp
            self.outstanding_token.save()

        access = self.token_obj.access_token

        self.access_exp = timezone.make_aware(timezone.datetime.fromtimestamp(access['exp']))
        self.access = str(access)

        return self

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            self.outstanding_token = OutstandingToken.objects.get(token=sha1(attrs['token'].encode('utf-8')).hexdigest())
        except OutstandingToken.DoesNotExist:
            raise serializers.ValidationError(_('Token is invalid.'))

        return attrs

    def create(self, validated_data):
        self.outstanding_token.delete()
        return self
