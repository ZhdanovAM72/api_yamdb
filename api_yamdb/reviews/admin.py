from django.contrib import admin

from reviews.models import Comment, Review, User


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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
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
