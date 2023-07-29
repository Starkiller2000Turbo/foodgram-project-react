from typing import Any, Dict, List

from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
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
from users.models import Favorite, Purchase


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
    filter_backends = (DjangoFilterBackend,)

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

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        """Фильтрация списка выдаваемых элементов по параметрам.

        Args:
            queryset: Список всех объектов.

        Returns:
            Список объектов с учётом поля tags запроса.
        """
        queryset = super().filter_queryset(queryset)
        tags = self.request.query_params.get('tags', None)

        if tags is not None:
            queryset = queryset.filter(tags__slug__contains=tags)

        return queryset


@api_view(['POST', 'DELETE'])
def favorite(
    request: AuthenticatedHttpRequest,
    pk: str,
) -> HttpResponse:
    """Обработка запросов к списку избранных рецептов.

    Args:
        request: Передаваемый запрос.
        pk: id рецепта.

    Returns:
        Информацию о рецепте: если рецепт добавлен.
        Ничего: в случае удаления рецепта.
        Информацию об ошибке: в прочих случаях.
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


@api_view(['POST', 'DELETE'])
def purchase(
    request: AuthenticatedHttpRequest,
    pk: str,
) -> HttpResponse:
    """Обработка запросов к списку покупок.

    Args:
        request: Передаваемый запрос.
        pk: id рецепта.

    Returns:
        Информацию о рецепте: если рецепт добавлен.
        Ничего: в случае удаления рецепта.
        Информацию об ошибке: в прочих случаях.
    """
    recipe = get_object_or_404(Recipe, id=pk)
    if request.method == 'POST':
        if recipe not in request.user.purchases.all():
            Purchase.objects.create(recipe=recipe, user=request.user)
            return Response(
                RecipeNestedSerializer(
                    recipe,
                ).data,
            )
        return Response(
            {
                'errors': 'невозможно добавить в список покупок второй раз',
            },
        )
    if not Purchase.objects.filter(
        recipe=recipe,
        user=request.user,
    ).exists():
        return Response(
            {'errors': 'рецепта нет в избранном'},
        )
    Purchase.objects.filter(recipe=recipe, user=request.user).delete()
    return Response()


@api_view(['GET'])
def shopping_cart(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Обработка запросов к списку покупок.

    Args:
        request: Передаваемый запрос.

    Returns:
        Файл со списком покупок пользователя.
    """
    cart: Dict[str, List[Any]] = dict()
    purchases = request.user.purchases.all()
    for purchase in purchases:
        ingredients = purchase.ingredients.all()
        for ingredient in ingredients:
            if ingredient.name in cart.keys():
                cart[ingredient.name][1] += ingredient.recipe_ingredients.get(
                    recipe=purchase,
                ).amount
            else:
                cart[ingredient.name] = [
                    ingredient.measurement_unit,
                    ingredient.recipe_ingredients.get(recipe=purchase).amount,
                ]
    file_data = ''
    for key in cart.keys():
        file_data += f'{key} ({cart[key][0]})- {cart[key][1]}\n'
    response = HttpResponse(
        file_data,
        content_type='application/text charset=utf-8',
    )
    response[
        'Content-Disposition'
    ] = 'attachment; filename="shopping_cart.txt"'
    return response
