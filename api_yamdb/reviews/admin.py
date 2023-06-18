from django.contrib import admin

from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title, User
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка админки для пользователей."""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    list_editable = ('role',)
    search_fields = ('role', 'username')
    list_filter = ('role', 'username')
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройки админ-панели категорий."""

    empty_value_display = '-отсутствует-'
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройки админ-панели жанров."""

    empty_value_display = '-отсутствует-'
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройки админ-панели произведений."""

    empty_value_display = '-отсутствует-'
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )
    list_filter = ('name',)
    search_fields = ('name', 'year', 'category')


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """Класс настройки соответствия жанров и произведений."""

    empty_value_display = '-отсутствует-'
    list_display = (
        'pk',
        'genre',
        'title'
    )
    list_filter = ('genre',)
    search_fields = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка админ-панели для отзывов."""

    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('title', 'text')
    list_filter = ('pub_date', 'author')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка админ-панели для комментариев."""

    list_display = (
        'pk',
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review', 'text')
    list_filter = ('pub_date', 'author')
    empty_value_display = '-пусто-'
