from typing import Any, Dict, Optional

from django.core.exceptions import ValidationError
from django.forms import Form


class RecipeFilterForm(Form):
    """Форма для валидации фильтрации по логическим полям модели рецепта."""

    def clean_is_favorited(self) -> Optional[Dict[str, Any]]:
        """Функция для валидации значения is_favorited.

        Returns:
            Данные, если они валидны.

        Raises:
            ValidationError: Если данные не валидны.
        """
        cleaned_data = super(RecipeFilterForm, self).clean()
        is_favorited = cleaned_data.get(  # type:ignore[union-attr]
            'is_favorited',
        )

        if is_favorited not in [0, 1, None]:
            raise ValidationError(
                '0 - False, 1 - True, другие значения недопустимы',
            )

        return cleaned_data

    def clean_is_in_shopping_cart(self) -> Optional[Dict[str, Any]]:
        """Функция для валидации значения is_in_shopping_cart.

        Returns:
            Данные, если они валидны.

        Raises:
            ValidationError: Если данные не валидны.
        """
        cleaned_data = super(RecipeFilterForm, self).clean()
        is_in_shopping_cart = cleaned_data.get(  # type:ignore[union-attr]
            'is_in_shopping_cart',
        )

        if is_in_shopping_cart not in [0, 1, None]:
            raise ValidationError(
                '0 - False, 1 - True, другие значения недопустимы',
            )

        return cleaned_data
