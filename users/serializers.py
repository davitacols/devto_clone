from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False},
        }

    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']
        extra_kwargs = {
            'profile_picture': {'required': False},
        }
