from django.contrib import admin

from users.models import Favorite, Following, Purchase, User


class FavoriteAdmin(admin.ModelAdmin):
    """Представление модели пользователя в админ-зоне."""

    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user',)
    empty_value_display = '-пусто-'


class FollowingAdmin(admin.ModelAdmin):
    """Представление модели пользователя в админ-зоне."""

    list_display = ('user', 'following')
    search_fields = ('user', 'following')
    list_filter = ('user',)
    empty_value_display = '-пусто-'


class PurchaseAdmin(admin.ModelAdmin):
    """Представление модели пользователя в админ-зоне."""

    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user',)
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    """Представление модели пользователя в админ-зоне."""

    list_display = ('username', 'email', 'first_name', 'last_name', 'password')
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Following, FollowingAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(User, UserAdmin)
