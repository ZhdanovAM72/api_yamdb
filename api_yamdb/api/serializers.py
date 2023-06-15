from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import AbstractUser

from reviews.models import User
from reviews.validators import me_validator


class AdminUsersSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей для админа/модератора."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class AnyUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class TokenSerializer(serializers.ModelSerializer):
    """Сериализотор токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class LoginSerializer(serializers.ModelSerializer):
    """Сериализатор получения кода на почту пользователя."""
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(me_validator, AbstractUser.username_validator)
    )

    def validate_username(self, value):
        return me_validator(value)

    class Meta:
        model = User
        fields = ('username', 'email')
