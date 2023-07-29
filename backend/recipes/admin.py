from typing import List

from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    """Представление модели ингредиента в админ-зоне."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    """Представление модели тега в админ-зоне."""

    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'color')
    empty_value_display = '-пусто-'


class IngredientInlineAdmin(admin.TabularInline):
    """Представление модели ингредиента в рецепте."""

    model = Recipe.ingredients.through
    readonly_fields = ('measurement_unit',)

    def measurement_unit(self, obj: RecipeIngredient) -> str:
        """Отображение поля единиц измерения для ингредиента в рецепте.

        Args:
            obj: Модель связи рецепт-ингредиент.

        Returns:
            Единицы измерения ингредиента.
        """
        return obj.ingredient.measurement_unit


class TagInlineAdmin(admin.TabularInline):
    """Представление модели тега в рецепте."""

    model = Recipe.tags.through


class RecipeAdmin(admin.ModelAdmin):
    """Представление модели рецепта в админ-зоне."""

    list_display = (
        'name',
        'author',
        'text',
        'image',
        'cooking_time',
        'get_tags',
        'get_ingredients',
    )
    search_fields = ('name', 'text')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'
    inlines = [IngredientInlineAdmin, TagInlineAdmin]
    readonly_fields = ('favorited',)

    def get_tags(self, obj: Recipe) -> List[str]:
        """Отображение списка тегов рецепта.

        Args:
            obj: Модель рецепта.

        Returns:
            Список полей slug используемых тегов.
        """
        return [tag.slug for tag in obj.tags.all()]

    def get_ingredients(self, obj: Recipe) -> List[str]:
        """Отображение списка ингредиентов рецепта.

        Args:
            obj: Модель рецепта.

        Returns:
            Список полей name используемых ингредиентов.
        """
        return [ingredient.name for ingredient in obj.ingredients.all()]

    def favorited(self, obj: Recipe) -> int:
        """Отображение количества добавлений рецепта в избранное.

        Args:
            obj: Модель рецепта.

        Returns:
            Количество добавлений рецепта в избранное.
        """
        return obj.selected.count()

    favorited.short_description = 'Добавлено в избранное'  # type: ignore
    get_tags.short_description = 'Теги'  # type: ignore
    get_ingredients.short_description = 'Ингредиенты'  # type: ignore


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
