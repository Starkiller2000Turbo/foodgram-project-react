from django.conf import settings
from django.db import models

from users.models import User


class AuthorTextModel(models.Model):
    """Модель с текстом и автором."""

    author = models.ForeignKey(
        User,
        verbose_name='автор',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='описание',
        help_text='Введите текст',
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Задание текстового представления модели.

        Returns:
            Поле text данной модели.
        """
        return self.text[:settings.TEXT_LENGTH]  # fmt: skip
