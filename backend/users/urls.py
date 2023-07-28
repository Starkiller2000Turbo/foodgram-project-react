from django.urls import include, path

from users import views

app_name = '%(app_label)s'

urlpatterns = [
    path(
        'users/subscriptions/',
        views.get_followings,
        name='get_followings',
    ),
    path(
        'users/<int:pk>/subscribe/',
        views.follow_unfollow,
        name='follow_unfollow',
    ),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
