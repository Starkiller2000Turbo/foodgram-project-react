from django.db.models import Model
from django.http import HttpRequest
from rest_framework import permissions, viewsets


class ReadOnly(permissions.BasePermission):
    """Разрешение на чтение всеми пользователями."""

    def has_permission(
        self,
        request: HttpRequest,
        view: viewsets.ModelViewSet,
    ) -> bool:
        """Проверка общего разрешения.

        Args:
            request: Передаваемый запрос.
            view: ViewSet, для которого проверяется разрешение.

        Returns:
            True или False в зависимости от наличия разрешения.
        """
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(
        self,
        request: HttpRequest,
        view: viewsets.ModelViewSet,
        obj: Model,
    ) -> bool:
        """Проверка разрешения на уровне объекта.

        Args:
            request: Передаваемый запрос.
            view: ViewSet, для которого проверяется разрешение.
            obj: Модель, с которой взаимодействует пользователь.

        Returns:
            True.
        """
        return True
