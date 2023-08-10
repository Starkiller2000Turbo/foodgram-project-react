from django.db.models import QuerySet
from django.http import HttpResponse


def shopping_file(cart: QuerySet) -> HttpResponse:
    """Функция для создания файла со списком покупок.

    Args:
        cart: Список ингредиентов.

    Returns:
        HTTPResponse с файлом списка покупок.
    """
    file_data = 'Список покупок\n'
    for purchase in cart:
        file_data += ' '.join(
            [
                f'·{purchase.get("ingredient__name")}',
                f'({purchase.get("ingredient__measurement_unit")})-',
                f'{purchase.get("amount")}\n',
            ],
        )
    response = HttpResponse(
        file_data,
        content_type='application/text charset=utf-8',
    )
    response[
        'Content-Disposition'
    ] = 'attachment; filename="shopping_cart.txt"'
    return response
