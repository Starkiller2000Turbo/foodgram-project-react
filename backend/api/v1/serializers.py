from rest_framework import serializers

from recipes.models import Ingredient, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиента."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тега."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
