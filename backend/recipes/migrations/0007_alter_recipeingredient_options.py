# Generated by Django 4.2.3 on 2023-07-27 18:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "recipes",
            "0006_alter_recipeingredient_options_ingredient_amount_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipeingredient",
            options={
                "default_related_name": "recipe_inredients",
                "verbose_name": "Ингредиент рецепта",
                "verbose_name_plural": "Ингредиенты рецепта",
            },
        ),
    ]
