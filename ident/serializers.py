# pylint: disable=missing-module-docstring
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User

class UserCreationSerializer(serializers.ModelSerializer): # pylint: disable=missing-class-docstring,abstract-method

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = User
        fields = ('email', 'username', 'password',)

    def validate(self, attrs):
        validate_password(attrs['password'], user=User(**attrs))
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
