from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import IngredientViewSet, TagViewSet

app_name = '%(app_label)s'

router = DefaultRouter()

router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls')),
]
