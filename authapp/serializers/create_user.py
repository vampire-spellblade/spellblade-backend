from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)

    def validate(self, attrs):
        validate_password(attrs['password'], user=User(**attrs))
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
