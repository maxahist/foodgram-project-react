from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='название')
    color = models.CharField(max_length=7,
                             verbose_name='цвет')
    slug = models.SlugField(unique=True,
                            verbose_name='слаг',
                            max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return self.slug


class Food(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='название продукта')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='единица измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='автор',
                               related_name='recipe',
                               )
    name = models.CharField(max_length=255,
                            verbose_name='название')
    image = models.ImageField('image',
                              upload_to='food/')
    text = models.TextField(verbose_name='описание')
    ingredients = models.ManyToManyField(Food,
                                         verbose_name='ингридиеты',
                                         through='FoodRecipe')
    tags = models.ManyToManyField(Tag,
                                  verbose_name='тэг',
                                  through='TagRecipe')
    cooking_time = models.IntegerField(verbose_name='время приготовления',
                                       validators=[MinValueValidator(1)])
    pub_date = models.DateTimeField(verbose_name='дата',
                                    auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            related_name='tagr',
                            verbose_name='тэг')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='tagr',
                               verbose_name='рецепт')

    class Meta:
        verbose_name = 'тэг в рецеате'
        verbose_name_plural = 'тэги в рецептах'

    def __str__(self):
        return f'{self.tag} в {self.recipe}'


class FoodRecipe(models.Model):
    food = models.ForeignKey(Food,
                             on_delete=models.CASCADE,
                             verbose_name='ингредиенты',
                             related_name='food')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe',
                               verbose_name='рецепт')
    amount = models.IntegerField(verbose_name='колтичество',
                                 validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'ингредиенты в рецептах'

    def __str__(self):
        return f'в {self.recipe} {self.amount} {self.food}'


class ShoppingBasket(models.Model):
    recipe = models.ForeignKey(Recipe,
                               verbose_name='рецепт',
                               related_name='cart',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             verbose_name='пользователь',
                             related_name='cart',
                             on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'],
            name='уже в корзине'
        )]
        verbose_name = 'карзина покупок'
        verbose_name_plural = 'карзины покупок'

    def __str__(self):
        return f'{self.recipe} в корзине у {self.user}'


class Favorites(models.Model):
    recipe = models.ForeignKey(Recipe,
                               verbose_name='рецепт',
                               related_name='favorites',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             verbose_name='пользователь',
                             related_name='favorites',
                             on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'],
            name='уже в избранном'
        )]
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'
