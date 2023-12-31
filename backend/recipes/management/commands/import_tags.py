import csv
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    """Команда для импорта ингредиентов из файла."""

    def handle(self, *args: Any, **options: Any) -> None:
        """Функция для импорта ингредиентов из файла.

        Args:
            *args: Передаваемые позиционные аргументы.
            **options: Передаваемые именованные аргументы.
        """
        print(  # noqa: T201
            'Importing data from:',
            settings.DATA_IMPORT_LOCATION,
        )
        with open(
            f'{settings.DATA_IMPORT_LOCATION}/tags.csv',
            'r',
            encoding='utf-8-sig',
        ) as csv_file:
            counter = 0
            data = csv.reader(csv_file)
            for name, color, slug in data:
                _, created = Tag.objects.get_or_create(
                    name=name,
                    color=color,
                    slug=slug,
                )
                if created:
                    counter += 1
            print(  # noqa: T201
                f'Import complete, imported {counter} tags',
            )
