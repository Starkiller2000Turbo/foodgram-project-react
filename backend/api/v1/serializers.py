from collections import OrderedDict
from typing import Any, List, Optional

from django.core.exceptions import ValidationError
from rest_framework import serializers

from core.serializers import Base64ImageField
from core.types import ComplexSerializerData
from recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag
from users.serializers import UserReadSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения модели ингредиента."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientNestedSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения модели ингредиента."""

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        read_only=False,
        queryset=Ingredient.objects.all(),
    )
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True,
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
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


class TagNestedSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тега."""

    id = serializers.PrimaryKeyRelatedField(
        source='tag.id',
        read_only=False,
        queryset=Ingredient.objects.all(),
    )
    name = serializers.CharField(source='tag.name', read_only=True)
    color = serializers.CharField(source='tag.color', read_only=True)
    slug = serializers.CharField(source='tag.slug', read_only=True)

    class Meta:
        model = RecipeTag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецепта."""

    author = UserReadSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)
    ingredients = IngredientNestedSerializer(many=True)
    tags = TagNestedSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipe


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецепта."""

    author = UserReadSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)
    ingredients = IngredientNestedSerializer(many=True, required=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=True,
    )

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipe

    def to_representation(self, instance: Recipe) -> Recipe:
        """Преобразование сериализатора для чтения.

        Args:
            instance: Модель рецепта.

        Returns:
            Представление сериализатора для чтения.
        """
        return RecipeReadSerializer(context=self.context).to_representation(
            instance,
        )

    def validate_ingredients(
        self,
        data: List[OrderedDict[str, Any]],
    ) -> Optional[List[OrderedDict[str, Any]]]:
        """Валидация данных поля ingredients.

        Args:
            data: Информация из поля ingredients.

        Raises:
            ValidationError: Ингредиентов с заданными параметрами нет.

        Returns:
            Информация из поля ingredients, если не было ошибки.
        """
        ingredient_ids = set()
        if data:
            for ingredient_data in data:
                ingredient = ingredient_data.get('ingredient').get('id')
                ingredient_id = ingredient.id
                if ingredient_id in ingredient_ids:
                    raise ValidationError(
                        'Ингредиенты не уникальны:'
                        f' минимум два с id {ingredient_id}',
                    )
                ingredient_ids.add(ingredient_id)
            return data
        return None

    def validate_tags(self, data: List[Tag]) -> Optional[List[Tag]]:
        """Валидация данных поля ingredients.

        Args:
            data: Информация из поля ingredients.

        Raises:
            ValidationError: Ингредиентов с заданными параметрами нет.

        Returns:
            Информация из поля ingredients, если не было ошибки.
        """
        tag_ids = set()
        if data:
            for tag in data:
                tag_id = tag.id
                if tag_id in tag_ids:
                    raise ValidationError(
                        f'Теги не уникальны: минимум два с id {tag_id}',
                    )
                tag_ids.add(tag_id)
            return data
        return None

    def add_ingredients(
        self,
        instance: Recipe,
        ingredients_data: List[OrderedDict[str, Any]],
    ) -> None:
        """Функция для создания связи рецептов и ингредиентов.

        Args:
            instance: Модель рецепта, дли которой создаются связи.
            Ingredients_data: Информация об ингредиентах.
        """
        recipeingredients = [
            RecipeIngredient(
                recipe=instance,
                ingredient_id=ingredient_data.get('ingredient').get('id').id,
                amount=ingredient_data.get('amount'),
            )
            for ingredient_data in ingredients_data
        ]
        RecipeIngredient.objects.bulk_create(recipeingredients)

    def update(
        self,
        instance: Recipe,
        validated_data: ComplexSerializerData,
    ) -> Recipe:
        """Изменение существующего рецепта.

        Args:
            instance: Существующая модель рецепта.
            validated_data: Прошедшие валидацию данные.

        Returns:
            Преобразованную модель рецепта
        """
        ingredients_data = validated_data.pop('ingredients', [])
        instance.ingredients.all().delete()
        self.add_ingredients(instance, ingredients_data)
        tags = validated_data.pop('tags', [])
        instance.tags.all().delete()
        for tag in tags:
            RecipeTag.objects.create(recipe=instance, tag=tag)
        return super().update(instance, validated_data)

    def create(self, validated_data: ComplexSerializerData) -> Recipe:
        """Создание нового рецепта.

        Args:
            validated_data: Прошедшие валидацию данные.

        Returns:
            Созданную модель рецепта
        """
        ingredients_data = validated_data.pop('ingredients', [])
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(
            **validated_data,
            author=self.context['request'].user,
        )
        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)
        self.add_ingredients(recipe, ingredients_data)
        return recipe
