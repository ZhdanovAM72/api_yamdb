from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.mixins import CreateListDestroyViewSet
from api.permissions import AnonReadOnly, AuthorOrModeratorsOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleViewingSerializer, TitleEditingSerializer)
from reviews.models import Category, Genre, Title


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleViewingSerializer
    permission_classes = (AnonReadOnly,
                          AuthorOrModeratorsOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        """Определяет сериализатор в зависимости от типа запроса."""
        if self.request.method == 'GET':
            return TitleEditingSerializer
        return TitleViewingSerializer
