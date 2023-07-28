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


class RecipeIngredientAdmin(admin.ModelAdmin):
    """Представление модели ингредиента в админ-зоне."""

    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')
    empty_value_display = '-пусто-'


class RecipeTagAdmin(admin.ModelAdmin):
    """Представление модели ингредиента в админ-зоне."""

    list_display = ('recipe', 'tag')
    search_fields = ('recipe', 'tag')
    list_filter = ('recipe', 'tag')
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    """Представление модели ингредиента в админ-зоне."""

    list_display = (
        'author',
        'text',
        'name',
        'image',
        'cooking_time',
    )
    search_fields = ('name', 'text')
    list_filter = ('author',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(Tag, TagAdmin)
