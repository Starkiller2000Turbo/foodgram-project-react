import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """Поле изображения на основании кодировки base64."""

    def to_internal_value(self, data: str) -> str:
        """Декодирование изображения из base64.

        Args:
            data: Строка, содержащая кодировку base64.

        Returns:
            Команду to_internal_value для декодированных данных.
        """
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(
                    imgstr,
                ),
                name='temp.' + ext,
            )  # type: ignore[assignment]

        return super().to_internal_value(data)
