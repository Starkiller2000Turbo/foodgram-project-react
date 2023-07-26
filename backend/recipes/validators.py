import string

from django.core.exceptions import ValidationError


def validate_color(value: str) -> None:
    """Валидация соответствия поля color представлению HEX.

    Args:
        value: Проверяемая строка.

    Raises:
        ValidationError: Если строка не соответствует представлению HEX.
    """
    if value[0] != '#' or not all(
        [
            symbol in tuple(string.digits + string.ascii_uppercase[:6])
            for symbol in value[1:]
        ],
    ):
        raise ValidationError(
            'Это поле должно содержать код цвета в кодировке'
            ' HEX, начиная с  символа #',
        )
