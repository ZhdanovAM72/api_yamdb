from django.core.exceptions import ValidationError
from django.utils import timezone

from api_yamdb.settings import USER_ME


def me_validator(value):
    """Проверяем недопустимое значение в поле username."""

    if value == USER_ME:
        raise ValidationError('Запрещено использовать'
                              f'имя пользователя {USER_ME}!')
    return value


def validate_year(value):
    """Проверяем допустимость значения в поле year."""

    if value > timezone.now().year:
        raise ValidationError(
            'Год не может быть больше текущего года.'
        )
 