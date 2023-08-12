from django.db.models import Exists, OuterRef, QuerySet, Sum, Case, When, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from api.v1.filters import RecipeFilterSet
from api.v1.permissions import AuthorOrReadOnly
from api.v1.serializers import (
    FavoriteSerializer,
    FollowingCreateSerializer,
    FollowingSerializer,
    IngredientSerializer,
    PurchaseSerializer,
    RecipeNestedSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)
from core.filters import NameStartsSearchFilter
from core.types import AuthenticatedHttpRequest
from core.utils import shopping_file
from recipes.models import (
    Favorite,
    Ingredient,
    Purchase,
    Recipe,
    RecipeIngredient,
    Tag,
)
from users.models import Following, User


class FollowingView(views.APIView):
    """Класс для создания подписок и их удаления."""

    def post(
        self,
        request: AuthenticatedHttpRequest,
        pk: str,
    ) -> HttpResponse:
        """Функция для создания подписки на автора.

        Args:
            request: Передаваемый запрос.
            pk: id модели автора.

        Returns:
            Данные автора, в случае успешной подписки.
        """
        serializer = FollowingCreateSerializer(
            data={'user': request.user.id, 'following': pk},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            FollowingSerializer(
                get_object_or_404(User, id=pk),
                context={'request': request},
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(
        self,
        request: AuthenticatedHttpRequest,
        pk: str,
    ) -> HttpResponse:
        """Функция для удаления подписки на автора.

        Args:
            request: Передаваемый запрос.
            pk: id модели автора.

        Returns:
            Статус 204.
        """
        get_object_or_404(
            Following,
            following__id=pk,
            user=request.user,
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowingViewSet(generics.ListAPIView):
    """View для получения списка подписок."""

    serializer_class = FollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Функция для получения подписок пользователя.

        Returns:
            Queryset, содержащий подписки пользователя.
        """
        return User.objects.filter(followers__user=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели ингредиента."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (NameStartsSearchFilter,)
    search_fields = ('^name',)


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
        user_id = self.request.user.id
        return queryset.annotate(
            is_in_shopping_cart=Exists(
                Purchase.objects.filter(
                    user_id=user_id,
                    recipe__id=OuterRef('id'),
                ),
            ),
            is_favorited=Exists(
                Favorite.objects.filter(
                    user_id=user_id,
                    recipe__id=OuterRef('id'),
                ),
            ),
        )

    def create_connection(
        self,
        serializer: Serializer,
        request: AuthenticatedHttpRequest,
        pk: str,
    ) -> HttpResponse:
        """Функция для создания объектов связи пользователя и рецепта.

        Args:
            serializer: Сериализатор модели связи пользователя и рецепта.
            request: Передаваемый запрос.
            pk: Уникальный id рецепта.
        """
        serializer = serializer(data={'user': request.user.id, 'recipe': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipe = get_object_or_404(Recipe, id=pk)
        return Response(
            RecipeNestedSerializer(
                recipe,
                context={'request': request},
            ).data,
            status=status.HTTP_201_CREATED,
        )

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
        return self.create_connection(FavoriteSerializer, request, pk)

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
        return self.create_connection(PurchaseSerializer, request, pk)

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
        cart = (
            RecipeIngredient.objects.filter(
                recipe__purchases__user=request.user,
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
            .order_by('ingredient__name')
        )
        return shopping_file(cart)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели тега."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
