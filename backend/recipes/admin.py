from django.contrib import admin
from django.utils.safestring import mark_safe

from recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Представление модели ингредиента в админ-зоне."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'


@admin.register(Tag)
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
    min_num = 1

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
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Представление модели рецепта в админ-зоне."""

    list_display = (
        'name',
        'id',
        'author',
        'text',
        'show_image',
        'cooking_time',
        'get_tags',
        'get_ingredients',
        'favorited',
    )
    search_fields = ('name', 'text')
    list_filter = ('name', 'author', 'tags__tag')
    empty_value_display = '-пусто-'
    inlines = [IngredientInlineAdmin, TagInlineAdmin]
    readonly_fields = ('favorited', 'id')

    @admin.display(description='Теги')
    def get_tags(self, obj: Recipe) -> int:
        """Отображение списка тегов рецепта.

        Args:
            obj: Модель рецепта.

        Returns:
            Список полей slug используемых тегов.
        """
        return obj.tags.all().count()

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj: Recipe) -> int:
        """Отображение списка ингредиентов рецепта.

        Args:
            obj: Модель рецепта.

        Returns:
            Список полей name используемых ингредиентов.
        """
        return obj.ingredients.all().count()

    @admin.display(description='Добавлено в избранное')
    def favorited(self, obj: Recipe) -> int:
        """Отображение количества добавлений рецепта в избранное.

        Args:
            obj: Модель рецепта.

        Returns:
            Количество добавлений рецепта в избранное.
        """
        return obj.favorited.all().count()

    @admin.display(description='Изображение')
    def show_image(self, obj: Recipe) -> int:
        """Отображение количества добавлений рецепта в избранное.

        Args:
            obj: Модель рецепта.

        Returns:
            Количество добавлений рецепта в избранное.
        """
        return mark_safe(f'<img src={obj.image.url} width="80" height="60">')
