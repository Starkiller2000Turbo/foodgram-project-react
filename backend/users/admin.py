from typing import List

from django.contrib import admin

from users.models import User


class FavoriteInlineAdmin(admin.TabularInline):
    """Представление модели пользователя в админ-зоне."""

    model = User.favorites.through


class FollowingInlineAdmin(admin.TabularInline):
    """Представление модели пользователя в админ-зоне."""

    model = User.followings.through
    fk_name = 'user'


class PurchaseInlineAdmin(admin.TabularInline):
    """Представление модели пользователя в админ-зоне."""

    model = User.purchases.through


class UserAdmin(admin.ModelAdmin):
    """Представление модели пользователя в админ-зоне."""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'get_favorites',
        'get_followings',
        'get_purchases',
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
    inlines = [FavoriteInlineAdmin, FollowingInlineAdmin, PurchaseInlineAdmin]

    def get_favorites(self, obj: User) -> List[str]:
        """Отображение списка избранного пользователя.

        Args:
            obj: Модель пользователя.

        Returns:
            Список избранных рецептов пользователя.
        """
        return [recipe.name for recipe in obj.favorites.all()]

    def get_followings(self, obj: User) -> List[str]:
        """Отображение списка подписок пользователя.

        Args:
            obj: Модель пользователя.

        Returns:
            Список подписок пользователя.
        """
        return [user.username for user in obj.followings.all()]

    def get_purchases(self, obj: User) -> List[str]:
        """Отображение списка покупок пользователя.

        Args:
            obj: Модель пользователя.

        Returns:
            Список покупок пользователя.
        """
        return [recipe.name for recipe in obj.purchases.all()]

    get_favorites.short_description = 'Избранное'  # type: ignore
    get_followings.short_description = 'Подписки'  # type: ignore
    get_purchases.short_description = 'Список покупок'  # type: ignore


admin.site.register(User, UserAdmin)
