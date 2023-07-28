from collections import OrderedDict
from typing import Any, List, Union

ListSerializerData = List[OrderedDict[str, Union[str, int]]]
SerializerData = OrderedDict[str, Union[str, int]]
ComplexSerializerData = OrderedDict[str, Any]
