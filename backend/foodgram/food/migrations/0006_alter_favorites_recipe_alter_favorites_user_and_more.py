# Generated by Django 4.1.7 on 2023-03-24 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food', '0005_rename_time_recipe_cooking_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='food.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='shoppingbasker',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='food.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppingbasker',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
