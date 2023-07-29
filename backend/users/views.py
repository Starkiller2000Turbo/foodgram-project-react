from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.types import AuthenticatedHttpRequest
from users.models import Following, User
from users.serializers import FollowingSerializer


@api_view(['POST', 'DELETE'])
def follow_unfollow(
    request: AuthenticatedHttpRequest,
    pk: str,
) -> HttpResponse:
    """Обработка запроса на подписку на определённого пользователя.

    Args:
        request: Передаваемый запрос.
        username: логин автора, на которого подписываются

    Returns:
        Рендер страницы редактирования поста.
    """
    following = get_object_or_404(User, id=pk)
    if request.method == 'POST':
        if (
            following != request.user
            and request.user not in following.followers.all()
        ):
            print(following.followers.all())
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


@api_view(['GET'])
def get_followings(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Обработка запроса на подписку на определённого пользователя.

    Args:
        request: Передаваемый запрос.
        username: логин автора, на которого подписываются

    Returns:
        Рендер страницы редактирования поста.
    """
    user = request.user
    followings = user.followings
    return Response(
        FollowingSerializer(
            followings,
            many=True,
            context={'request': request},
        ).data,
    )
