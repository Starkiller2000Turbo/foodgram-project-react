from typing import List

from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag


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

    model = RecipeIngredient
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

    model = RecipeTag


class RecipeAdmin(admin.ModelAdmin):
    """Представление модели рецепта в админ-зоне."""

    list_display = (
        'name',
        'id',
        'author',
        'text',
        'image',
        'cooking_time',
        'get_tags',
        'get_ingredients',
    )
    search_fields = ('name', 'text')
    list_filter = ('name', 'author', 'tags__tag')
    empty_value_display = '-пусто-'
    inlines = [IngredientInlineAdmin, TagInlineAdmin]
    readonly_fields = ('favorited', 'id')

    def get_tags(self, obj: Recipe) -> List[str]:
        """Отображение списка тегов рецепта.

        Args:
            obj: Модель рецепта.

        Returns:
            Список полей slug используемых тегов.
        """
        return list(obj.tags.all().values_list('tag__slug', flat=True))

    def get_ingredients(self, obj: Recipe) -> List[str]:
        """Отображение списка ингредиентов рецепта.

        Args:
            obj: Модель рецепта.

        Returns:
            Список полей name используемых ингредиентов.
        """
        return list(
            obj.ingredients.all().values_list('ingredient__name', flat=True),
        )

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
