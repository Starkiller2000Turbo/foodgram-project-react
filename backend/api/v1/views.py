from http import HTTPStatus

from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.v1.serializers import IngredientSerializer
from recipes.models import Ingredient
from users.models import User
from users.serializers import UserSerializer, UserReadSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in (
            'retrieve',
            'list',
        ):
            return UserReadSerializer
        return UserSerializer

    def me(self, request):
        """Функция для получения информации о своем пользователе"""
        user = request.user
        if request.method == 'GET':
            serializer = UserReadSerializer(user)
            return Response(serializer.data, status=HTTPStatus.OK)
        serializer = UserReadSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=HTTPStatus.OK)
