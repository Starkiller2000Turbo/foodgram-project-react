from rest_framework import serializers

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

    recipes = RecipeNestedSerializer(many=True)
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
