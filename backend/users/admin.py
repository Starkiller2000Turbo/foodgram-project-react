from typing import Any, Dict, List, Optional

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db.models.fields.related import ForeignKey
from django.forms import ModelChoiceField
from django.http import HttpRequest
from django.urls import resolve

from users.models import User


class FavoriteInlineAdmin(admin.TabularInline):
    """Представление модели пользователя в админ-зоне."""

    model = User.favorites.through


class FollowingInlineAdmin(admin.TabularInline):
    """Представление модели пользователя в админ-зоне."""

    model = User.followings.through
    fk_name = 'user'

    def get_parent_object_from_request(
        self,
        request: HttpRequest,
    ) -> Optional[User]:
        """Функция для получения отображаемого пользователя.

        Args:
            request: Передаваемый запрос.

        Returns:
            Объект User: При наличии данных об отображаемом пользователе.
            None: В случае отсутствия данных о пользователе.
        """
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(
                pk=resolved.kwargs['object_id'],
            )
        return None

    def formfield_for_foreignkey(
        self,
        db_field: ForeignKey,
        request: HttpRequest,
        **kwargs: Dict[str, Any],
    ) -> ModelChoiceField:
        """Функция для получения объектов для выбора.

        Args:
            db_field:
            request: Передаваемый запрос.
            **kwargs:

        Returns:
            Объект User: При наличии данных об отображаемом пользователе.
            None: В случае отсутствия данных о пользователе.
        """
        user = self.get_parent_object_from_request(request)
        if db_field.name == 'following' and user:
            kwargs[
                'queryset'
            ] = User.objects.exclude(  # type:ignore[assignment]
                Q(username=user.username),
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PurchaseInlineAdmin(admin.TabularInline):
    """Представление модели пользователя в админ-зоне."""

    model = User.purchases.through


class UserAdmin(DefaultUserAdmin):
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
admin.site.unregister(Group)
