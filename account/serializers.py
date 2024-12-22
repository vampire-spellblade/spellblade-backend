from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',)

    def validate(self, attrs):
        password1 = attrs.pop('password1')
        password2 = attrs.pop('password2')

        if password1 != password2:
            raise serializers.ValidationError({
                'password1': [_('The passwords do not match.'),]
            })

        attrs['password'] = password1
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UpdateUserPersonalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.pop('first_name', instance.first_name)
        instance.last_name = validated_data.pop('last_name', instance.last_name)
        instance.save()
        return instance

class UpdateUserEmailSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('current_password', 'email',)

    def validate(self, attrs):
        email = attrs.get('email')

        if not self.instance.check_password(attrs.pop('current_password')):
            raise serializers.ValidationError({
                'current_password': [_('The password is incorrect.'),]
            })

        if self.instance.email == email:
            raise serializers.ValidationError({
                'email': [_('The new email cannot be the same as the current one.'),]
            })

        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data.pop('email', instance.email)
        instance.save()
        return instance

class UpdateUserPasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('current_password', 'new_password1', 'new_password2',)

    def validate(self, attrs):
        current_password = attrs.pop('current_password')
        new_password1 = attrs.pop('new_password1')
        new_password2 = attrs.pop('new_password2')

        if not self.instance.check_password(current_password):
            raise serializers.ValidationError({
                'current_password': [_('The password is incorrect.'),]
            })

        new_password1_errors = {}

        if current_password == new_password1:
            if 'new_password1' not in new_password1_errors:
                new_password1_errors['new_password1'] = []
            new_password1_errors['new_password1'].append(_('The new password cannot be the same as the current one.'))

        if new_password1 != new_password2:
            if 'new_password1' not in new_password1_errors:
                new_password1_errors['new_password1'] = []
            new_password1_errors['new_password1'].append(_('The passwords do not match.'))

        if len(new_password1_errors) > 0:
            raise serializers.ValidationError(new_password1_errors)

        attrs['new_password'] = new_password1
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('new_password'))
        instance.save()
        return instance
