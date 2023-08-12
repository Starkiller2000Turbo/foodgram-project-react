import io
from django.http import FileResponse
from django.db.models import QuerySet
from django.http import HttpResponse
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def shopping_file(cart: QuerySet) -> HttpResponse:
    """Функция для создания файла со списком покупок.

    Args:
        cart: Список ингредиентов.

    Returns:
        HTTPResponse с файлом списка покупок.
    """
    buffer = io.BytesIO()
    p = Canvas(buffer, pagesize=A4)
    pdfmetrics.registerFont(TTFont('DejaVuSerif','DejaVuSerif.ttf', 'UTF-8'))
    x_start = 40
    y_start = 800
    p.setFont('DejaVuSerif', 25)
    p.drawString(x_start, y_start, 'Список покупок')
    p.line(0,790,1000,790)
    if not cart:
        p.setFont('DejaVuSerif', 16)
        y_start -= 30
        p.drawString(x_start, y_start, '-список пуст-')
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="shopping-list.pdf", content_type='application/pdf charset=utf-8')
    p.setFont('DejaVuSerif', 16)
    for purchase in cart:
        y_start -= 30
        if y_start < 0:
            p.showPage()
            p.setFont('DejaVuSerif', 16)
            y_start = 800
        p.drawString(x_start, y_start, ' '.join(
            [
                f'·{purchase.get("ingredient__name")}',
                f'({purchase.get("ingredient__measurement_unit")})-',
                f'{purchase.get("amount")}',
            ],
        ),
        )
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="shopping-list.pdf", content_type='application/pdf charset=utf-8')
