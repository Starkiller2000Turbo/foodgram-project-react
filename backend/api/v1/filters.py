from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet

from recipes.models import Recipe


class RecipeFilterSet(FilterSet):
    """Фильтр для моделей рецептов."""

    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
