from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


class UsernameValidator(UnicodeUsernameValidator):
    """Расширение валидации username."""

    max_length = 150


def me_validator(value):
    """Проверяем недопустимое значение в поле username."""

    if value == 'me':
        raise ValidationError('Запрещено использовать имя пользователя "me"!')
    return value
