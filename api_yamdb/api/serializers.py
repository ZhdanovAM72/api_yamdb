from rest_framework import serializers

from reviews.models import User


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
    class Meta:
        model = User
        fields = ('username', 'email')
