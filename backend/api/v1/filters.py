from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet

from api.v1.forms import RecipeFilterForm
from core.filters import filter_boolean_by_int
from recipes.models import Recipe
from users.models import User


class RecipeFilterSet(FilterSet):
    """Фильтр для моделей рецептов."""

    tags = filters.AllValuesMultipleFilter(field_name='tags__tag__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(
        method=filter_boolean_by_int,
        field_name='is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method=filter_boolean_by_int,
        field_name='is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        form = RecipeFilterForm
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
