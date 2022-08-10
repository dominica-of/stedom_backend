from abc import ABC

from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User

        fields = [
            "id",
            "email",
            "full_name",
            "specification",
            "password",
            "is_active",
            "date_joined",
        ]

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            },
            'date_joined': {'read_only': True},
            'is_active': {'read_only': True},
            'email': {'required': True},
            'full_name': {'required': True},

        }

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'full_name': self.validated_data.get('full_name', ''),
            'specification': self.validated_data.get('specification', ''),
            'password': self.validated_data.get('password', '')
        }

    @staticmethod
    def validate_password(value):
        password_validation.validate_password(value)
        return value


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    class Meta:
        extra_kwargs = {
            'refresh': {'required': True},
        }

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class EmptySerializer(serializers.Serializer):
    pass
