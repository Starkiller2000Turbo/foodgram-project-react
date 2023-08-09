from typing import Any, Dict, List

from django.db.models import Exists, OuterRef, QuerySet, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from api.v1.filters import RecipeFilterSet
from api.v1.serializers import (
    FavoriteSerializer,
    FollowingSerializer,
    IngredientSerializer,
    PurchaseSerializer,
    RecipeNestedSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)
from api.v1.permissions import AuthorOrReadOnly
from core.filters import NameStartsSearchFilter
from core.types import AuthenticatedHttpRequest
from core.utils import shopping_file
from recipes.models import Ingredient, Purchase, Recipe, Tag, RecipeIngredient
from users.models import Favorite, Following, User


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели ингредиента."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (NameStartsSearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели тега."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет, обрабатывающий запросы к рецептам."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer
    permission_classes = [AuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def get_queryset(self) -> QuerySet:
        """Функция для добавления к рецептам дополнительных полей.

        Returns:
            QuerySet, содержащий рецепты с дополнительными полями.
        """
        queryset = super(RecipeViewSet, self).get_queryset()
        user = self.request.user
        recipes = queryset.annotate(
            is_in_shopping_cart=Exists(
                Purchase.objects.filter(
                    user=user,
                    recipe__name=OuterRef('name'),
                ),
            ),
            is_favorited=Exists(
                Favorite.objects.filter(
                    user=user,
                    recipe__name=OuterRef('name'),
                ),
            ),
        )
        return recipes

    def create_connection(
        self,
        serializer: Serializer,
        request: AuthenticatedHttpRequest,
        pk: str,
    ) -> None:
        """Функция для создания объектов связи пользователя и рецепта.

        Args:
            serializer: Сериализатор модели связи пользователя и рецепта.
            request: Передаваемый запрос.
            pk: Уникальный id рецепта.
        """
        serializer = serializer(data={'user': request.user.id, 'recipe': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @action(detail=True, methods=['post'])
    def favorite(
        self,
        request: AuthenticatedHttpRequest,
        pk: str,
    ) -> HttpResponse:
        """Обработка запросов к списку избранных рецептов.

        Args:
            request: Передаваемый запрос.
            pk: id рецепта.

        Returns:
            Информацию о рецепте: если рецепт добавлен.
            Ничего: в случае удаления рецепта.
            Информацию об ошибке: в прочих случаях.
        """
        self.create_connection(FavoriteSerializer, request, pk)
        return Response(
            RecipeNestedSerializer(
                get_object_or_404(Recipe, id=pk),
                context={'request': request},
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @favorite.mapping.delete
    def delete_favorite(
        self,
        request: AuthenticatedHttpRequest,
        pk: str,
    ) -> HttpResponse:
        """Обработка запросов к списку избранных рецептов.

        Args:
            request: Передаваемый запрос.
            pk: id рецепта.

        Returns:
            Информацию о рецепте: если рецепт добавлен.
            Ничего: в случае удаления рецепта.
            Информацию об ошибке: в прочих случаях.
        """
        get_object_or_404(Favorite, recipe__id=pk, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def shopping_cart(
        self,
        request: AuthenticatedHttpRequest,
        pk: str,
    ) -> HttpResponse:
        """Обработка добавления рецепта в список покупок.

        Args:
            request: Передаваемый запрос.
            pk: id рецепта.

        Returns:
            Информацию о рецепте: если рецепт добавлен.
            Ничего: в случае удаления рецепта.
            Информацию об ошибке: в прочих случаях.
        """
        self.create_connection(PurchaseSerializer, request, pk)
        return Response(
            RecipeNestedSerializer(
                get_object_or_404(Recipe, id=pk),
                context={'request': request},
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(
        self,
        request: AuthenticatedHttpRequest,
        pk: str,
    ) -> HttpResponse:
        """Обработка запросов к списку избранных рецептов.

        Args:
            request: Передаваемый запрос.
            pk: id рецепта.

        Returns:
            Информацию о рецепте: если рецепт добавлен.
            Ничего: в случае удаления рецепта.
            Информацию об ошибке: в прочих случаях.
        """
        get_object_or_404(Purchase, recipe__id=pk, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(
        self,
        request: AuthenticatedHttpRequest,
    ) -> HttpResponse:
        """Обработка запросов к списку покупок.

        Args:
            request: Передаваемый запрос.

        Returns:
            Файл со списком покупок пользователя.
        """
        cart = RecipeIngredient.objects.filter(recipe__buyers__user=request.user).values('ingredient__name', 'ingredient__measurement_unit').annotate(amount=Sum('amount')).order_by('ingredient__name')
        return shopping_file(cart)


@api_view(['POST', 'DELETE'])
def follow_unfollow(
    request: AuthenticatedHttpRequest,
    pk: str,
) -> HttpResponse:
    """Обработка запросов на подписку и отмену подписки.

    Args:
        request: Передаваемый запрос.
        pk: id автора.

    Returns:
        Информацию ою авторе: в случае подписки.
        Ничего: в случае удаления подписки.
        Информацию об ошибке: в прочих случаях.
    """
    following = get_object_or_404(User, id=pk)
    if request.method == 'POST':
        if (
            following != request.user
            and request.user not in following.followers.all()
        ):
            Following.objects.create(following=following, user=request.user)
            return Response(
                FollowingSerializer(
                    following,
                    context={'request': request},
                ).data,
            )
        return Response(
            {
                'errors': 'невозможно подписаться на самого себя'
                'или подписаться второй раз',
            },
        )
    if not Following.objects.filter(
        following=following,
        user=request.user,
    ).exists():
        return Response(
            {'errors': 'невозможно отписаться, подписки не существует'},
        )
    Following.objects.filter(following=following, user=request.user).delete()
    return Response()


class FollowingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели ингредиента."""

    serializer_class = FollowingSerializer
    permission_classes = (permissions.IsAuthenticated)

    def get_queryset(self) -> QuerySet:
        """Функция для получения подписок пользователя.

        Returns:
            Queryset, содержащий подписки пользователя.
        """
        return self.request.user.followings.all()
