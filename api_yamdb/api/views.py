from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404

from api_yamdb.settings import EMAIL_ADMIN
from api.mixins import CreateListDestroyViewSet
from api.permissions import (AdminOnly,
                             AdminAuthorOrReadOnly,
                             AuthorOrModeratorsOrReadOnly, 
                             AnonReadOnly,
                             AdminOrSuperuserOnly)
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleViewingSerializer, TitleEditingSerializer,
                             AnyUserSerializer, AdminUsersSerializer,
                             LoginSerializer, TokenSerializer,
                             CommentSerializer, ReviewSerializer)
from reviews.models import Category, Genre, Title, User, Review


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AnonReadOnly,
                          AdminOrSuperuserOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AnonReadOnly,
                          AdminOrSuperuserOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleViewingSerializer
    permission_classes = (AnonReadOnly,
                          AdminOrSuperuserOnly,)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        """Определяет сериализатор в зависимости от типа запроса."""
        if self.request.method == 'GET':
            return TitleViewingSerializer
        return TitleEditingSerializer


class UserViewSet(ModelViewSet):
    """ViewSet пользователей."""

    queryset = User.objects.all()
    serializer_class = AdminUsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,),
        url_path='me',
        detail=False,
        url_name='me',
    )
    def get_patch_user_info(self, request):
        serializer = AdminUsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = AdminUsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = AnyUserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiUserSignup(APIView):
    """Код подтверждения для получения токена."""

    permission_classes = (AllowAny,)

    @staticmethod
    def emails_send(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
            from_email=EMAIL_ADMIN,
        )
        email.send()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_text = (
            f'Привет {user.username}!'
            f'Это код для API: {user.confirmation_code}'
        )
        email_data = {
            'email_body': email_text,
            'to_email': user.email,
            'email_subject': 'API код для доступа!'
        }
        self.emails_send(email_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetApiToken(APIView):
    """Создание токена по коду из письма."""

    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response({'username': 'Пользователь не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            api_token = RefreshToken.for_user(user).access_token
            return Response({'token': str(api_token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Указан неверный код доступа к API.'},
            status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(ModelViewSet):
    """ViewSet отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          AuthorOrModeratorsOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """ViewSet комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          AuthorOrModeratorsOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
