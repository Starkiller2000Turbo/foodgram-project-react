# Generated by Django 4.2.3 on 2023-07-28 12:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0016_recipeingredient_recipe_ingredient_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipeingredient",
            options={
                "default_related_name": "recipe_ingredients",
                "verbose_name": "Ингредиент рецепта",
                "verbose_name_plural": "Ингредиенты рецепта",
            },
        ),
        migrations.AlterModelOptions(
            name="recipetag",
            options={
                "default_related_name": "recipe_tags",
                "verbose_name": "Тег рецепта",
                "verbose_name_plural": "Теги рецепта",
            },
        ),
        migrations.AlterField(
            model_name="recipeingredient",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.ingredient",
                verbose_name="ингредиент",
            ),
        ),
        migrations.AlterField(
            model_name="recipeingredient",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.recipe",
                verbose_name="рецепт",
            ),
        ),
    ]