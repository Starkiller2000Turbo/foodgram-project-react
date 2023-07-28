from rest_framework import serializers

from core.serializers import Base64ImageField
from recipes.models import Recipe


class RecipeNestedSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецепта."""

    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        model = Recipe
