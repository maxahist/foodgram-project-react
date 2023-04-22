import logging

from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from food.models import (Favorites, Food, FoodRecipe, Recipe, ShoppingBasket,
                         Tag)
from rest_framework import serializers
from users.serializers import UserSerializer


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Food


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag
        read_only_fields = ['name',
                            'color',
                            'slug']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('food__amount')
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return not user.is_anonymous and obj.favorites.filter(
            user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return not user.is_anonymous and obj.cart.filter(
            user=user).exists()

    def validate(self, data):
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        data.update({
            'tags': tags,
            'ingredients': ingredients,
            'author': self.context.get('request').user
        })
        return data

    def create_ingredients(self, recipe, ingredients):
        irgredient_list = []
        for item in ingredients:
            logging.info(item)
            ingredient = FoodRecipe(recipe=recipe,
                                    food_id=item.get('id'),
                                    amount=item.get('amount'))
            irgredient_list.append(ingredient)
        FoodRecipe.objects.bulk_create(irgredient_list)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, obj, validated_data):

        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            obj.tags.clear()
            for tag in tags:
                obj.tags.add(tag)
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            obj.ingredients.clear()
            self.create_ingredients(obj, ingredients)
        return super().update(obj, validated_data)


class CartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingBasket
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorites
        fields = ('id', 'name', 'image', 'cooking_time')
