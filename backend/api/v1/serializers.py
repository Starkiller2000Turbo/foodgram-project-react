from django.core.exceptions import ValidationError
from rest_framework import serializers

from core.serializers import Base64ImageField
from core.types import ComplexSerializerData, ListSerializerData
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

    id = serializers.IntegerField(read_only=False)
    amount = serializers.IntegerField(default=0)
    name = serializers.CharField(read_only=True)
    measurement_unit = serializers.CharField(read_only=True)

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

    def to_representation(self, instance: Ingredient) -> Ingredient:
        """Преобразование сериализатора для чтения.

        Args:
            instance: Модель ингредиента.

        Returns:
            Представление сериализатора для чтения.
        """
        representation = super().to_representation(instance)
        if isinstance(self.root, serializers.ListSerializer):
            recipe = self.root.child._instance
        else:
            recipe = self.root.instance
        representation['name'] = instance.name
        representation['measurement_unit'] = instance.measurement_unit
        representation['amount'] = instance.recipe_ingredients.get(
            recipe=recipe,
        ).amount
        return representation


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


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецепта."""

    author = UserReadSerializer(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True, default=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True, default=True)
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientNestedSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
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
        self._instance = instance
        representation = super(RecipeSerializer, self).to_representation(
            instance,
        )
        representation['tags'] = TagSerializer(instance.tags, many=True).data
        return representation

    def validate_ingredients(
        self,
        data: ListSerializerData,
    ) -> ListSerializerData:
        """Валидация данных поля ingredients.

        Args:
            data: Информация из поля ingredients.

        Raises:
            ValidationError: Ингредиентов с заданными параметрами нет.

        Returns:
            Информация из поля ingredients, если не было ошибки.
        """
        for ingredient_data in data:
            ingredient_id = ingredient_data.get('id')
            if not Ingredient.objects.filter(
                id=ingredient_id,
            ).exists():  # type: ignore[misc]
                raise ValidationError(
                    f'Ингредиента с id {ingredient_id} не существует',
                )
        return data

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
        if ingredients_data:
            instance.recipe_ingredients.all().delete()
            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data.get('id')
                ingredient_amount = ingredient_data.get('amount')
                ingredient = Ingredient.objects.get(id=ingredient_id)
                RecipeIngredient.objects.create(
                    recipe=instance,
                    ingredient=ingredient,
                    amount=ingredient_amount,
                )
        tags = validated_data.pop('tags', [])
        if tags:
            instance.recipe_tags.all().delete()
            for tag in tags:
                RecipeTag.objects.create(recipe=instance, tag=tag)
        instance.name = validated_data.pop('name', instance.name)
        instance.text = validated_data.pop('text', instance.text)
        instance.image = validated_data.pop('image', instance.image)
        instance.cooking_time = validated_data.pop(
            'cooking_time',
            instance.cooking_time,
        )
        instance.save()
        return instance

    def create(self, validated_data: ComplexSerializerData) -> Recipe:
        """Создание нового рецепта.

        Args:
            validated_data: Прошедшие валидацию данные.

        Returns:
            Созданную модель рецепта
        """
        ingredients_data = validated_data.pop('ingredients', [])
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        if ingredients_data:
            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data.get('id')
                ingredient_amount = ingredient_data.get('amount')
                ingredient = Ingredient.objects.get(id=ingredient_id)
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=ingredient_amount,
                )
        if tags:
            for tag in tags:
                RecipeTag.objects.create(recipe=recipe, tag=tag)
        return recipe
