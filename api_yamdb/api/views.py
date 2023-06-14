from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import EmailMessage

from api_yamdb.settings import EMAIL_ADMIN
from reviews.models import User
from api.serializers import (AnyUserSerializer,
                             AdminUsersSerializer,
                             LoginSerializer,
                             TokenSerializer)
from api.permissions import AdminOnly


class UserViewSet(ModelViewSet):
    """ViewSet пользователей."""

    queryset = User.objects.all()
    serializer_class = AdminUsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly)
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,),
        url_path='me',
        detail=True,
    )
    def get_patch_user_info(self, request):
        serializer = AdminUsersSerializer(request.user)

        if request.method == 'PATH':
            if request.user.is_admin:
                serializer = AdminUsersSerializer(
                    request.user,
                    partial=True,
                    data=request.data,
                )
            else:
                serializer = AnyUserSerializer(
                    request.user,
                    partial=True,
                    data=request.data,
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


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
            f'Это твой код для подключения к API: {user.confirmation_code}'
        )
        email_data = {
            'email_body': email_text,
            'to_email': user.email,
            'email_subject': 'API код для доступа.'
        }
        self.send_email(email_data)
        return Response(status=status.HTTP_200_OK)


class GetApiToken(APIView):
    """Создание токена по коду из письма."""

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
