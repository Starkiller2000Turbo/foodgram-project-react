from typing import Union

from django.db.models import QuerySet
from rest_framework import filters


class NameStartsSearchFilter(filters.SearchFilter):
    """Класс фильтрации с регулярными выражениями по параметру name."""

    search_param = 'name'


def filter_boolean_by_int(
    queryset: QuerySet,
    name: str,
    value: Union[str, int],
) -> QuerySet:
    """Функция для фильтрации поля BooleanFilter по цифрам 0,1.

    Args:
        queryset: Передаваемые объекты в виде Queryset.
        name: Поле, по которому происходит фильтрация.
        value: Переданный параметр фильтрации.

    Returns:
        Queryset объектов, отфильтрованный по заданному значению.
    """
    if value is not None:
        if value == 0:
            return queryset.filter(**{name: False})
        if value == 1:
            return queryset.filter(**{name: True})
    return queryset
