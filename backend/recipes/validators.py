import string

from django.core.exceptions import ValidationError


def number_in_hex(value):
    allowed = tuple(string.digits + string.ascii_uppercase[:6])
    return all([symbol in allowed for symbol in value])


def validate_color(value):
    if value[0] != '#' or not number_in_hex(value[1:]):
        raise ValidationError(
            'Это поле должно содержать код цвета в кодировке'
            ' HEX, начиная с  символа #',
        )
