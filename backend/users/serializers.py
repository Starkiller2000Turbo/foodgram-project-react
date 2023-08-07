from typing import Dict, List, Union

from rest_framework import serializers

from core.types import SerializerStrData
from recipes.serializers import RecipeNestedSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data: SerializerStrData) -> User:
        """Метод для создания пользователя с хэшированным паролем.

        Args:
            validated_data: Данные пользователя, прошедшие валидацию.

        Returns:
            Созданную модель пользователя.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserReadSerializer(serializers.ModelSerializer):
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
        )

    def get_is_subscribed(self, obj: User) -> bool:
        """Формирование значения поля is_subscribed.

        Args:
            obj: Модель пользователя.

        Returns:
            Наличие подписки текущего пользователя на данного.
        """
        return self.context['request'].user in obj.followers.all()


class FollowingSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения подписки."""

    recipes = serializers.SerializerMethodField('paginated_recipes')
    recipes_count = serializers.IntegerField(source='recipes.count')
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
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj: User) -> bool:
        """Формирование значения поля is_subscribed.

        Args:
            obj: Модель пользователя.

        Returns:
            Наличие подписки текущего пользователя на данного.
        """
        return self.context['request'].user in obj.followers.all()

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
            recipes = obj.recipes.order_by('id')[: int(recipes_limit)]
        else:
            recipes = obj.recipes.all()
        return RecipeNestedSerializer(recipes, many=True).data
