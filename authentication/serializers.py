from abc import ABC

from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers

from authentication.models import Booking

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
            "rating",
            "user_type",
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
            'user_type': {'required': True},
            'full_name': {'required': True},

        }

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'full_name': self.validated_data.get('full_name', ''),
            'user_type': self.validated_data.get('full_name', ''),
            'specification': self.validated_data.get('specification', ''),
            'password': self.validated_data.get('password', '')
        }



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


class BookingSerializer(serializers.ModelSerializer):
    instructor = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email',
                                              required=False, allow_null=True)
    learner = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email',
                                           required=False, allow_null=True)

    instructor_full_name = serializers.SerializerMethodField('get_instructor_full_name')
    learner_full_name = serializers.SerializerMethodField('get_learner_full_name')

    def get_instructor_full_name(self, obj):
        return obj.instructor.full_name

    def get_learner_full_name(self, obj):
        return obj.learner.full_name

    class Meta:
        model = Booking
        fields = [
            'date_time',
            'instructor',
            'instructor_full_name',
            'learner',
            'learner_full_name',

        ]

        extra_kwargs = {
            'instructor_full_name': {'read_only': True},
            'learner_full_name': {'read_only': True},
        }


class EmptySerializer(serializers.Serializer):
    pass
