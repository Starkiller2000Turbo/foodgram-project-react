from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Класс пагинации с переменным количеством объектов на странице."""

    page_size_query_param = 'limit'
