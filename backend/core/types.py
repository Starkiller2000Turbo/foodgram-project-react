from collections import OrderedDict
from typing import Any, List, Union

from django.http import HttpRequest

from users.models import User

ListSerializerData = List[OrderedDict[str, Union[str, int]]]
SerializerData = OrderedDict[str, Union[str, int]]
ComplexSerializerData = OrderedDict[str, Any]


class AuthenticatedHttpRequest(HttpRequest):
    """Класс запроса авторизованным пользователем."""

    user: User
