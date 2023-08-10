from rest_framework import filters


class NameStartsSearchFilter(filters.SearchFilter):
    """Класс фильтрации с регулярными выражениями по параметру name."""

    search_param = 'name'
