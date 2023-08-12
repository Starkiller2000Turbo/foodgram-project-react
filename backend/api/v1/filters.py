from django_filters.rest_framework import filters, FilterSet

from recipes.models import Recipe, Tag


class RecipeFilterSet(FilterSet):
    """Фильтр для моделей рецептов."""

    tags = filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), to_field_name='slug', field_name='tags__slug',)
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
