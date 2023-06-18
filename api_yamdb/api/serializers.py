from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comment, Review, User


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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        current_request = self.context['request'].method == 'POST'
        if current_request and Review.objects.filter(
            author=author, title=title_id
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв к этому произведению')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категории.
    """
    class Meta:
        fields = ('name', 'slug', )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанра.
    """
    class Meta:
        fields = ('name', 'slug', )
        model = Genre


class TitleViewingSerializer(serializers.ModelSerializer):
    """
    Сериализатор произведения в режиме просмотра.
    """
    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.SerializerMethodField(
        read_only=True,
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title

    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg('score'))
        return obj["rating"]


class TitleEditingSerializer(serializers.ModelSerializer):
    """
    Сериализатор произведения в режиме создания/редактирования.
    """

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title
