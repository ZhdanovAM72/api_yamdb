from django.core.exceptions import ValidationError

from api_yamdb.settings import USER_ME


def me_validator(value):
    """Проверяем недопустимое значение в поле username."""

    if value == USER_ME:
        raise ValidationError('Запрещено использовать'
                              f'имя пользователя {USER_ME}!')
    return value
