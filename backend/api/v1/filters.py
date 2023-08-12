from django_filters.rest_framework import filters, FilterSet

from recipes.models import Recipe, Tag
from users.models import User


class RecipeFilterSet(FilterSet):
    """Фильтр для моделей рецептов."""

    tags = filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), to_field_name='slug', field_name='tags__slug',)
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
    
    def __init__(self, *args, **kwargs):
        data = kwargs['data']
        author_data = data.get('author')
        if author_data == 'me':
            _mutable = data._mutable
            data._mutable = True
            data['author'] = kwargs['request'].user.id
            data._mutable = _mutable
        super(RecipeFilterSet, self).__init__(*args, **kwargs)
