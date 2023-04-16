from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet,
                    RecipeViewSet,
                    FoodViewSet)

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', FoodViewSet, basename='food')
router_v1.register('recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router_v1.urls)),

]
