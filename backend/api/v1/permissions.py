from django.http import HttpRequest
from rest_framework import permissions, viewsets

from recipes.models import Recipe


class AuthorOrReadOnly(permissions.BasePermission):
    """Разрешение изменение только автором."""

    def has_object_permission(
        self,
        request: HttpRequest,
        view: viewsets.ModelViewSet,
        obj: Recipe,
    ) -> bool:
        """Проверка авторства или безопасности запроса.

        Args:
            request: Передаваемый запрос.
            view: ViewSet, для которого проверяется разрешение.
            obj: Модель, с которой взаимодействует пользователь.

        Returns:
            True или False в зависимости от наличия разрешения.
        """
        return (request.method in permissions.SAFE_METHODS) | (
            obj.author == request.user
        )
