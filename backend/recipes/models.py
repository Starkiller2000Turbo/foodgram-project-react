from django.core.validators import MinValueValidator
from django.db import models

from core.models import AuthorTextModel
from recipes.validators import validate_color


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        """Представление модели при выводе.

        Returns:
            Строка поля name, используемого для представления модели.
        """
        return self.name


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, validators=[validate_color])
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        """Представление модели при выводе.

        Returns:
            Строка поля name, используемого для представления модели.
        """
        return self.name


class Recipe(AuthorTextModel):
    """Модель рецепта."""

    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='тег',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='ингредиент',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        unique=True,
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='время приготовления',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='название',
        unique=True,
    )

    class Meta:
        ordering = ['id']
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        """Задание текстового представления рецепта.

        Returns:
            Поле name данного рецепта.
        """
        return self.name


class RecipeTag(models.Model):
    """Модель связи рецепта и тега."""

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='тег',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'
        default_related_name = 'recipe_tags'
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'],
                name='recipe_tag',
            ),
        ]

    def __str__(self) -> str:
        """Задание текстового представления произведения.

        Returns:
            Строковое представление связи рецепта и тега.
        """
        return f'{self.recipe.name}, тег - {self.tag.name}'


class RecipeIngredient(models.Model):
    """Модель связи рецепта и ингредиента."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )
    amount = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        default_related_name = 'recipe_ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='recipe_ingredient',
            ),
        ]

    def __str__(self) -> str:
        """Задание текстового представления произведения.

        Returns:
            Строковое представление связи рецепта и ингредиента.
        """
        return f'{self.recipe.name}, ингредиент - {self.ingredient.name}'
