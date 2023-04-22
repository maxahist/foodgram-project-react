from django.contrib import admin
from django.contrib.admin import StackedInline

from .models import (Favorites, Food, FoodRecipe, Recipe, ShoppingBasket, Tag,
                     TagRecipe)


class FoodInline(StackedInline):
    model = FoodRecipe
    extra = 0


class TagInline(StackedInline):
    model = TagRecipe
    extra = 0


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'slug', 'color')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'text', 'cooking_time', 'favorites')
    search_fields = ('author__username', 'tags__name', 'name')
    list_filter = ('author__username', 'tags__name', 'name')
    empty_value_display = '-пусто-'
    inlines = (FoodInline, TagInline)

    def favorites(self, obj):
        return obj.favorites.count()


class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    search_fields = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    empty_value_display = '-пусто-'


class CartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    search_fields = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    empty_value_display = '-пусто-'


admin.site.register(Food, FoodAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorites, FavouritesAdmin)
admin.site.register(ShoppingBasket, CartAdmin)
