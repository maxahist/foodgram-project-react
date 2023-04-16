from api.serializers import Base64ImageField
from django.contrib.auth import get_user_model
from food.models import Recipe
from rest_framework import serializers

from .models import Subscription, User

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        extra_kwargs = {'password': {'write_only': 'True'}}

    def get_is_subscribed(self, obj):
        username = self.context.get('request').user
        return Subscription.objects.filter(sub__username=username,
                                           author=obj.id).exists()

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubSerializer(UserSerializer):
    email = serializers.CharField(source='author.email')
    id = serializers.IntegerField(source='author.id')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed', 'recipes',
                  'recipes_count')
        model = Subscription

    def get_recipes_count(self, obj):
        return obj.author.recipe.count()

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(sub=obj.sub,
                                           author=obj.author).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author)
        if self.context:
            limit = self.context.get('request').GET.get('recipes_limit')
            queryset = queryset[:int(limit)]
        return RecipeSerializer(queryset, many=True).data
