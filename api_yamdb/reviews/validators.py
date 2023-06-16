from django.core.exceptions import ValidationError


def me_validator(value):
    """Проверяем недопустимое значение в поле username."""

    if value == 'me':
        raise ValidationError('Запрещено использовать имя пользователя "me"!')
    return value
