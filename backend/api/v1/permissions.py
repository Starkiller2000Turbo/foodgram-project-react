from django.http import HttpRequest
from rest_framework import permissions, viewsets


class ReadOnly(permissions.BasePermission):
    def has_permission(
        self,
        request: HttpRequest,
        view: viewsets.ModelViewSet,
    ) -> bool:
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj) -> bool:
        return True
