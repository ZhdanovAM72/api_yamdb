from django.db import models
from django.contrib.auth.models import AbstractUser

TEXT_LENGTH = 25

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

CHOICE_ROLE = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    """Переопределяем модель пользователей."""
    username = models.CharField(
        verbose_name='Username пользователя',
        max_length=150,
        null=False,
        unique=True,
        blank=False,
    )
    email = models.EmailField(
        verbose_name='адрес электронной почты',
        max_length=254,
        null=False,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max(len(role_name) for role_name, role_dis in CHOICE_ROLE),
        default=USER,
        blank=True,
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user_data',
            )
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username[:TEXT_LENGTH]} {self.role}'
