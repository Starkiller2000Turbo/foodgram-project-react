from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    """Представление модели пользователя в админ-зоне."""

    list_display = ('username', 'email', 'first_name', 'last_name', 'password')
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
