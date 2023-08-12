from collections import OrderedDict
from typing import Any, Dict, List, Optional, Union

from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import exceptions, serializers

from core.constants import (
    MAX_POSITIVE_INTEGER_VALUE,
    MIN_POSITIVE_INTEGER_VALUE,
)
from core.types import ComplexSerializerData
from recipes.models import (
    Favorite,
    Ingredient,
    Purchase,
    Recipe,
    RecipeIngredient,
    Tag,
)
from users.models import Following, User


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели избранного."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'recipe'),
                message='Уже в избранном.',
            ),
        ]


class FollowingCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для модели избранного."""

    class Meta:
        model = Following
        fields = ('user', 'following')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'following'),
                message='Уже подписан.',
            ),
        ]

    def validate(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Функция для валидации полей сериализатора.

        Args:
            attrs: Словарь передаваемых параметров.

        Returns:
            Словарь передаваемых параметров, если они валидны.

        Raises:
            ValidationError: Если переданные данные не валидны.
        """
        super().validate(attrs)
        if attrs['user'] == attrs['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.',
            )
        return attrs


class PurchaseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели избранного."""

    class Meta:
        model = Purchase
        fields = ('user', 'recipe')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'recipe'),
                message='Уже в списке покупок.',
            ),
        ]


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_is_subscribed(self, obj: User) -> bool:
        """Формирование значения поля is_subscribed.

        Args:
            obj: Модель пользователя.

        Returns:
            Наличие подписки текущего пользователя на данного.
        """
        return self.context['request'].user in obj.followers.all()


class FollowingSerializer(UserSerializer):
    """Сериализатор для отображения подписки."""

    recipes = serializers.SerializerMethodField('paginated_recipes')
    recipes_count = serializers.IntegerField(source='recipes.count')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def paginated_recipes(self, obj: User) -> List[Dict[str, Union[str, int]]]:
        """Формирование списка рецептов пользователя.

        Args:
            obj: Модель пользователя.

        Returns:
            Список рецептов пользователя.
        """
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit',
        )
        if recipes_limit:
            try:
                recipes_limit = int(recipes_limit)
            except ValueError:
                raise exceptions.ParseError(
                    'recipes_limit должен быть целым числом',
                )
            return RecipeNestedSerializer(
                obj.recipes.order_by('id')[: int(recipes_limit)],
                many=True,
            ).data
        return RecipeNestedSerializer(obj.recipes.all(), many=True).data


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
        read_only=True,
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


class IngredientWriteSerializer(serializers.ModelSerializer):
    """Класс для создания связи ингредиента и рецепта."""

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        read_only=False,
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField(
        min_value=MIN_POSITIVE_INTEGER_VALUE,
        max_value=MAX_POSITIVE_INTEGER_VALUE,
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
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


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецепта."""

    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)
    ingredients = IngredientNestedSerializer(
        source='recipe_ingredient',
        many=True,
    )
    tags = TagSerializer(many=True)

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

    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientWriteSerializer(
        many=True,
        required=True,
        error_messages={'required': 'Выберите хотя бы 1 ингредиент'},
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=True,
        error_messages={'required': 'Выберите хотя бы 1 тег'},
    )
    cooking_time = serializers.IntegerField(
        min_value=MIN_POSITIVE_INTEGER_VALUE,
        max_value=MAX_POSITIVE_INTEGER_VALUE,
    )

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
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
        return RecipeReadSerializer(instance, context=self.context).data

    def validate(self, data: ComplexSerializerData) -> ComplexSerializerData:
        """Валидация данных поля ingredients.

        Args:
            data: Информация из поля ingredients.

        Raises:
            ValidationError: Ингредиентов с заданными параметрами нет.

        Returns:
            Информация из поля ingredients, если не было ошибки.
        """
        ingredients_data = data.get('ingredients')
        ingredient_ids = set()
        for ingredient_data in ingredients_data:  # type:ignore[union-attr]
            ingredient = ingredient_data.get(
                'ingredient',
            ).get(  # type:ignore[union-attr]
                'id',
            )
            ingredient_id = ingredient.id
            if ingredient_id in ingredient_ids:
                raise ValidationError(
                    'Ингредиенты не уникальны:'
                    f' минимум два с id {ingredient_id}',
                )
            ingredient_ids.add(ingredient_id)
        tags_data = data.get('tags')
        tag_ids = set()
        for tag in tags_data:  # type:ignore[union-attr]
            tag_id = tag.id
            if tag_id in tag_ids:
                raise ValidationError(
                    f'Теги не уникальны: минимум два с id {tag_id}',
                )
            tag_ids.add(tag_id)
        super().validate(data)
        return data

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
        recipeingredients = sorted(
            [
                RecipeIngredient(  # type:ignore[misc]
                    recipe=instance,
                    ingredient_id=ingredient_data.get(
                        'ingredient',
                    )
                    .get(  # type:ignore[union-attr]
                        'id',
                    )
                    .id,
                    amount=ingredient_data.get('amount'),
                )
                for ingredient_data in ingredients_data
            ],
            key=lambda obj: obj.ingredient.name,
        )
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
        instance.recipe_ingredient.all().delete()
        self.add_ingredients(instance, ingredients_data)
        tags = validated_data.pop('tags', [])
        instance.recipe_tag.all().delete()
        instance.tags.set(tags)
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
        recipe.tags.set(tags)
        self.add_ingredients(recipe, ingredients_data)
        return recipe
