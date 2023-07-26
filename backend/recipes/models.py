from django.db import models

from recipes.validators import validate_color


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(max_length=200)
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

    name = models.CharField(max_length=200)
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
