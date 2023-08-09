from django.db.models import QuerySet
from django.http import HttpResponse


def shopping_file(cart: QuerySet) -> HttpResponse:
    file_data = ''
    for purchase in cart:
        file_data += f'·{purchase.get("ingredient__name")} ({purchase.get("ingredient__measurement_unit")})- {purchase.get("amount")}\n'
    response = HttpResponse(
        file_data,
        content_type='application/text charset=utf-8',
    )
    response[
        'Content-Disposition'
    ] = 'attachment; filename="shopping_cart.txt"'
    return response