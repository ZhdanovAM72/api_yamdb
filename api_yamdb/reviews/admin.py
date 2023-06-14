from django.contrib import admin

from reviews.models import User


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
