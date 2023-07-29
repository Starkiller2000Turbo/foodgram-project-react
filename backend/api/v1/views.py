from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.v1.permissions import AuthorOrReadOnly, ReadOnly
from api.v1.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from core.types import AuthenticatedHttpRequest
from recipes.models import Ingredient, Recipe, Tag
from recipes.serializers import RecipeNestedSerializer
from users.models import Favorite


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели ингредиента."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (ReadOnly,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели тега."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (ReadOnly,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'color')


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет, обрабатывающий запросы к рецептам."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AuthorOrReadOnly]

    def perform_create(self, serializer: serializers.ModelSerializer) -> None:
        """Автоматическое добавление автора и логических полей.

        Args:
            serializer: сериализатор, содержащий информацию о рецепте.
        """
        serializer.save(
            author=self.request.user,
            is_favorited=False,
            is_in_shopping_cart=False,
        )


@api_view(['POST', 'DELETE'])
def favorite(
    request: AuthenticatedHttpRequest,
    pk: str,
) -> HttpResponse:
    """Обработка запроса на подписку на определённого пользователя.

    Args:
        request: Передаваемый запрос.
        username: логин автора, на которого подписываются

    Returns:
        Рендер страницы редактирования поста.
    """
    recipe = get_object_or_404(Recipe, id=pk)
    if request.method == 'POST':
        if recipe not in request.user.favorites.all():
            Favorite.objects.create(recipe=recipe, user=request.user)
            return Response(
                RecipeNestedSerializer(
                    recipe,
                ).data,
            )
        return Response(
            {
                'errors': 'невозможно добавить в избранное второй раз',
            },
        )
    if not Favorite.objects.filter(
        recipe=recipe,
        user=request.user,
    ).exists():
        return Response(
            {'errors': 'рецепта нет в избранном'},
        )
    Favorite.objects.filter(recipe=recipe, user=request.user).delete()
    return Response()
