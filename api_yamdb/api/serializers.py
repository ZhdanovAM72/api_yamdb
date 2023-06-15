from django.db.models import Avg

from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
        obj = obj.reviews.all().aggregate(rating=Avg("score"))
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
