from collections import OrderedDict
from typing import Any, List, Union

from django.http import HttpRequest

from users.models import User

SerializerData = OrderedDict[str, Union[str, int]]
SerializerStrData = OrderedDict[str, str]
ListSerializerData = List[SerializerData]
ComplexSerializerData = OrderedDict[str, Any]


class AuthenticatedHttpRequest(HttpRequest):
    """Класс запроса авторизованным пользователем."""

    user: User
