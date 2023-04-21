from django_filters.rest_framework import filters, FilterSet
from rest_framework.filters import SearchFilter

from food.models import Recipe


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(
        method='filter_favorites'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    ingredients = filters.CharFilter()

    class Meta:
        model = Recipe
        fields = ('author',
                  'tags',
                  'is_favorited')

    def filter_favorites(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(cart__user=self.request.user)
        return queryset


class FoodFilter(FilterSet):
    name = filters.CharFilter(field_name='name',
                              lookup_expr='icontains')
