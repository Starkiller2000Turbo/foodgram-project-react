from django.urls import include, path

from api.v1 import views

app_name = '%(app_label)s'

urlpatterns = [
    path(
        'users/subscriptions/',
        views.FollowingViewSet.as_view(),
        name='get_followings',
    ),
    path(
        'users/<int:pk>/subscribe/',
        views.FollowingView.as_view(),
        name='follow_unfollow',
    ),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
