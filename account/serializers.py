from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('email', 'first_name', 'last_name', 'password',)

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)
