# Generated by Django 3.2.16 on 2023-08-10 13:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='recipes',
                to=settings.AUTH_USER_MODEL,
                verbose_name='автор',
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(
                related_name='recipes',
                through='recipes.RecipeIngredient',
                to='recipes.Ingredient',
                verbose_name='ингредиент',
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(
                related_name='recipes',
                through='recipes.RecipeTag',
                to='recipes.Tag',
                verbose_name='тег',
            ),
        ),
        migrations.AddField(
            model_name='purchase',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='purchases',
                to='recipes.recipe',
                verbose_name='рецепт',
            ),
        ),
        migrations.AddField(
            model_name='purchase',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='purchases',
                to=settings.AUTH_USER_MODEL,
                verbose_name='пользователь',
            ),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement',
            ),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='favorites',
                to='recipes.recipe',
                verbose_name='рецепт',
            ),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='favorites',
                to=settings.AUTH_USER_MODEL,
                verbose_name='пользователь',
            ),
        ),
        migrations.AddConstraint(
            model_name='recipetag',
            constraint=models.UniqueConstraint(
                fields=('recipe', 'tag'), name='unique_recipe_tag'
            ),
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient',
            ),
        ),
    ]