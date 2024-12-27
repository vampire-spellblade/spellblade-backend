# pylint: disable=missing-module-docstring

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
#from .models import ()

User = get_user_model()

class UserCreationSerializer(serializers.ModelSerializer):
    '''Serializer for creating a new user'''

    class Meta: # pylint: disable=missing-class-docstring
        model = User
        fields = ('email', 'first_name', 'last_name', 'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs): # pylint: disable=missing-function-docstring
        validate_password(attrs['password'], user=User(**attrs))
        return attrs

    def create(self, validated_data): # pylint: disable=missing-function-docstring
        return User.objects.create_user(**validated_data)
