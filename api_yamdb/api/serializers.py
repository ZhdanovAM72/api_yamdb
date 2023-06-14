from django.db.models import Avg

from rest_framework import serializers

from reviews.models import Comment, Review, User


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
        fields = ('id', 'text', 'author', 'score', 'pub_date')

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

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        title_id = self.context['view'].kwargs.get('title_id')
        title = Title.objects.get(id=title_id)
        reviews = Review.objects.filter(title=title)

        average_value = reviews.aggregate(Avg('score'))
        title.rating = average_value['score__avg']
        title.save()

        return review

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.score = validated_data.get('score', instance.score)
        instance.save()

        title_id = self.context['view'].kwargs.get('title_id')
        title = Title.objects.get(id=title_id)
        reviews = Review.objects.filter(title=title)

        average_value = reviews.aggregate(Avg('score'))
        title.rating = average_value['score__avg']
        title.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
