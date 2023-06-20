from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from reviews.models import User
from api_yamdb.settings import EMAIL_ADMIN


def send_confirmation_code(request):
    """Отправляет confirmation_code пользователю на почту."""

    user = get_object_or_404(
        User,
        username=request.data.get('username'),
    )
    user.confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_mail(
        'Код для получения токена к API',
        f'Код подтверждения {user.confirmation_code}',
        f'{EMAIL_ADMIN}',
        [request.data.get('email')],
    )
 