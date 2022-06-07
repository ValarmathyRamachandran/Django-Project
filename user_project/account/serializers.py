from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'confirm_password',
        ]
        extra_kwargs = {'password': {'write_only': True}}
        required_fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']

    def save(self):
        user = User(email=self.validated_data['email'],
                    username=self.validated_data['username'],
                    )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Password must match.'})
        user.set_password(password)
        user.save()
        return user


class LoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password']
        required_fields = fields


class EmailSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email'
        ]
