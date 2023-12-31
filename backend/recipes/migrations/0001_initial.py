# Generated by Django 3.2.16 on 2023-08-10 13:27

import colorfield.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
                'default_related_name': 'favorites',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=200, verbose_name='название'),
                ),
                (
                    'measurement_unit',
                    models.CharField(
                        max_length=200, verbose_name='единица измерения'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
                'default_related_name': 'purchases',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'text',
                    models.TextField(
                        help_text='Введите текст', verbose_name='описание'
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        unique=True,
                        upload_to='recipes/images/',
                        verbose_name='картинка',
                    ),
                ),
                (
                    'cooking_time',
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1,
                                message='Время приготовления не может быть менее 1 минуты',
                            ),
                            django.core.validators.MaxValueValidator(
                                32767,
                                message='Время приготовления не может быть более 32767 минут',
                            ),
                        ],
                        verbose_name='время приготовления',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200, unique=True, verbose_name='название'
                    ),
                ),
                (
                    'created',
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-created', 'name'),
                'default_related_name': 'recipes',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200, unique=True, verbose_name='название'
                    ),
                ),
                (
                    'color',
                    colorfield.fields.ColorField(
                        default='#FFFFFF',
                        image_field=None,
                        max_length=18,
                        samples=None,
                        verbose_name='цвет',
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        max_length=200, unique=True, verbose_name='слаг'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'recipe',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='recipe_tag',
                        to='recipes.recipe',
                        verbose_name='рецепт',
                    ),
                ),
                (
                    'tag',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='recipe_tag',
                        to='recipes.tag',
                        verbose_name='тег',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Тег рецепта',
                'verbose_name_plural': 'Теги рецепта',
                'default_related_name': 'recipe_tag',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'amount',
                    models.PositiveSmallIntegerField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message='Количество не может быть менее 1'
                            ),
                            django.core.validators.MaxValueValidator(
                                32767,
                                message='Время приготовления не может быть более 32767 минут',
                            ),
                        ],
                    ),
                ),
                (
                    'ingredient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='recipe_ingredient',
                        to='recipes.ingredient',
                        verbose_name='ингредиент',
                    ),
                ),
                (
                    'recipe',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='recipe_ingredient',
                        to='recipes.recipe',
                        verbose_name='рецепт',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Ингредиент рецепта',
                'verbose_name_plural': 'Ингредиенты рецепта',
                'default_related_name': 'recipe_ingredient',
            },
        ),
    ]
