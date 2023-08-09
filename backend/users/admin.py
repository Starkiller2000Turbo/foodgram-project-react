from typing import Any, Dict, Optional

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db.models.fields.related import ForeignKey
from django.forms import ModelChoiceField
from django.http import HttpRequest
from django.urls import resolve

from recipes.models import Favorite, Purchase
from users.models import Following, User


class FavoriteInlineAdmin(admin.TabularInline):
    """Представление модели пользователя в админ-зоне."""

    model = Favorite


class FollowingInlineAdmin(admin.TabularInline):
    """Представление модели пользователя в админ-зоне."""

    model = Following
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

    model = Purchase


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    """Представление модели пользователя в админ-зоне."""

    list_display = (
        'username',
        'id',
        'email',
        'first_name',
        'last_name',
        'get_favorites',
        'get_followings',
        'get_purchases',
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    readonly_fields = ('id',)
    empty_value_display = '-пусто-'
    inlines = [FavoriteInlineAdmin, FollowingInlineAdmin, PurchaseInlineAdmin]

    @admin.display(description='Избранное')
    def get_favorites(self, obj: User) -> int:
        """Отображение списка избранного пользователя.

        Args:
            obj: Модель пользователя.

        Returns:
            Список избранных рецептов пользователя.
        """
        return obj.favorites.all().count()

    @admin.display(description='Подписки')
    def get_followings(self, obj: User) -> int:
        """Отображение списка подписок пользователя.

        Args:
            obj: Модель пользователя.

        Returns:
            Список подписок пользователя.
        """
        return obj.followings.all().count()

    @admin.display(description='Список покупок')
    def get_purchases(self, obj: User) -> int:
        """Отображение списка покупок пользователя.

        Args:
            obj: Модель пользователя.

        Returns:
            Список покупок пользователя.
        """
        return obj.purchases.all().count()


admin.site.unregister(Group)
