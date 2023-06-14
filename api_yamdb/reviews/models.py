from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator


TEXT_LENGTH = 25


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
    """Модель произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание произведения',
        db_index=True,
    )
    year = models.PositiveIntegerField(
        verbose_name='год выпуска',
        db_index=True,
        validators=[
            MaxValueValidator(
                int(datetime.now().year),
                message='Значение в поле не должно превышать текущий год.'
            )
        ],
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    description = models.TextField(
        verbose_name='Краткое описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class GenreTitle(models.Model):
    """Kласс, связывающий жанры и произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Произведение относится к жанру'
        verbose_name_plural = 'Произведение относится к жанрам'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} принадлежит жанру/ам {self.genre}'
