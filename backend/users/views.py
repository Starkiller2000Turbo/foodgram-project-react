from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.permissions import ReadOnly
from core.types import AuthenticatedHttpRequest
from users.models import Following, User
from users.serializers import FollowingSerializer


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
    permission_classes = (
        permissions.IsAuthenticated,
        ReadOnly,
    )

    def get_queryset(self) -> QuerySet:
        """Функция для получения подписок пользователя.

        Returns:
            Queryset, содержащий подписки пользователя.
        """
        return self.request.user.followings.all()
