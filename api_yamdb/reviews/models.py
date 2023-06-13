from django.db import models


class Title(models.Model):
    """Модель тайтла. Поля жанр и категории в тестовом режиме закомментил."""
    name = models.CharField(max_length=100)
    author = models.CharField(
        max_length=100,
        help_text='Автор произведения',
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Автор',
    )
    # category = models.ForeignKey(
    #     Category,
    #     help_text='Категория произведения',
    #     on_delete=models.CASCADE,
    #     related_name='titles',
    # )
    description = models.CharField(max_length=200)
    # genre = models.ForeignKey(
    #     Genre,
    #     on_delete=models.SET_NULL,
    #     related_name='titles',
    #     verbose_name='Жанр произведения',
    # )
    published = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    reviews_quantity = models.IntegerField()
    rating = models.IntegerField()

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name
