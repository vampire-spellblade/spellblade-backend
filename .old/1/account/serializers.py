class UserChangePersonalInfoSerializer(serializers.ModelSerializer):
    '''Serializer for updating user personal info'''

    class Meta: # pylint: disable=missing-class-docstring
        model = User
        fields = ('first_name', 'last_name',)

    def update(self, instance, validated_data): # pylint: disable=missing-function-docstring
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.save()
        return instance

class UserChangeEmailSerializer(serializers.ModelSerializer):
    '''Serializer for updating user email'''

    class Meta: # pylint: disable=missing-class-docstring
        model = User
        fields = ('email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs): # pylint: disable=missing-function-docstring
        if not self.instance.check_password(attrs['password']):
            raise serializers.ValidationError({'password': [_('Incorrect password')]})
        return attrs

    def update(self, instance, validated_data): # pylint: disable=missing-function-docstring
        instance.email = validated_data['email']
        instance.save()
        return instance

class UserChangePasswordSerializer(serializers.ModelSerializer):
    '''Serializer for updating user password'''
    new_password = serializers.CharField(write_only=True)

    class Meta: # pylint: disable=missing-class-docstring
        model = User
        fields = ('password', 'new_password',)
        extra_kwargs = {
            'password': {'write_only': True},
            'new_password': {'write_only': True},
        }

    def validate(self, attrs): # pylint: disable=missing-function-docstring
        if not self.instance.check_password(attrs['password']):
            raise serializers.ValidationError({'password': [_('Incorrect password')]})
        return attrs

    def update(self, instance, validated_data): # pylint: disable=missing-function-docstring
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
