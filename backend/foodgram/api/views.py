from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from food.models import (Favorites, Food, FoodRecipe, Recipe, ShoppingBasket,
                         Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import FoodFilter, RecipeFilter
from .paginations import CustomPaginator
from .permissions import IsOwnerOrReadOnly
from .serializers import (CartSerializer, FavoriteSerializer, FoodSerializer,
                          RecipeSerializer, TagSerializer)


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('^name',)
    filterset_class = FoodFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,)
            )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if self.request.method == 'POST':
            cart = ShoppingBasket.objects.create(user=user,
                                                 recipe=recipe)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        cart = get_object_or_404(ShoppingBasket, user=user,
                                 recipe=recipe)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,)
            )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if self.request.method == 'POST':
            favorite = Favorites.objects.create(user=user,
                                                recipe=recipe)
            serializer = FavoriteSerializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        favorite = get_object_or_404(Favorites, user=user,
                                     recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['GET'],
            permission_classes=(IsAuthenticated,)
            )
    def download_shopping_cart(self, request):
        user = request.user
        shop_cart = ShoppingBasket.objects.filter(user=user)
        if not shop_cart.exists():
            return Response('нет рецептов в корзине',
                            status=status.HTTP_400_BAD_REQUEST)

        ingrediets = FoodRecipe.objects.filter(
            recipe__cart__user=user).values('food__name',
                                            'food__measurement_unit').annotate(
            sum_=Sum('amount'))

        food_dict = {}
        for i in ingrediets:
            name = i["food__name"]
            amount = str(i["sum_"]) + " " + i["food__measurement_unit"]
            food_dict[name] = amount

        content = ('shopping_list \n')
        for key, value in food_dict.items():
            content += (f'{key}: {value} \n')
        return HttpResponse(
            content, headers={
                'Content-Type': 'text/plain',
                'Content-Disposition': 'attachment;'
                                       'filename="food_to_buy.txt"'}
        )
