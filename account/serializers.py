from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UpdateUserPersonalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.pop('first_name')
        instance.last_name = validated_data.pop('last_name')
        instance.save()
        return instance

class UpdateUserEmailSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('current_password', 'email',)

    def validate(self, attrs):
        if not self.instance.check_password(attrs.pop('current_password')):
            raise serializers.ValidationError({
                'current_password': [_('The password is incorrect.'),]
            })

        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data.pop('email')
        instance.save()
        return instance

class UpdateUserPasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('current_password', 'new_password',)

    def validate(self, attrs):
        if not self.instance.check_password(attrs.pop('current_password')):
            raise serializers.ValidationError({
                'current_password': [_('The password is incorrect.'),]
            })

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('new_password'))
        instance.save()
        return instance
