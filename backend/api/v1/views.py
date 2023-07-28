from rest_framework import filters, serializers, viewsets

from api.v1.permissions import AuthorOrReadOnly, ReadOnly
from api.v1.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.models import Ingredient, Recipe, Tag


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
