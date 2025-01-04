from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)

    def validate(self, attrs):
        try:
            validate_password(attrs['password'], user=User(**attrs))
        except Exception as e:
            # Using ValidationError here doesn't seem to work.
            # More specifically, the error is not caught if ValidationError is in use despite
            # the docs saying that that's what validate_password throws.
            raise serializers.ValidationError({'password': e.messages})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
