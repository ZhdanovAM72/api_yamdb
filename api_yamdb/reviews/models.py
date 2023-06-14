from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from reviews.validators import UsernameValidator, me_validator

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
        username_validator=(UsernameValidator(), me_validator),
        blank=False,
    )
    email = models.EmailField(
        verbose_name='адрес электронной почты',
        max_length=254,
        null=False,
        unique=True,
        blank=False,
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max(len(role_name) for role_name, role_dis in CHOICE_ROLE),
        choices=CHOICE_ROLE,
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

    REQUIRED_FIELDS = ('email', )

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


class Genre(models.Model):
    """Модель жанра."""
    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание жанра',
        db_index=True,
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание категории',
        db_index=True,
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Title(models.Model):
    """Модель тайтла."""
    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание произведения',
        db_index=True,
    )
    year = models.PositiveIntegerField(
        verbose_name='год выпуска',
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        help_text='Категория произведения',
        on_delete=models.CASCADE,
        related_name='titles',
        null=True,
    )
    description = models.TextField(
        verbose_name='Краткое описание',
        blank=True
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Review(models.Model):
    """Модель отзыва."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.text[:TEXT_LENGTH]


class Comment(models.Model):
    """Модель комментария."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв к произведению'
    )
    text = models.TextField(verbose_name='Комментарий на отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:TEXT_LENGTH]
