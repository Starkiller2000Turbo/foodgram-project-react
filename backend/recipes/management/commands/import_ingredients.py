import csv
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда для импорта ингредиентов из файла."""

    def handle(self, *args: Any, **options: Any) -> None:
        """Функция для импорта ингредиентов из файла.

        Args:
            *args: Передаваемые позиционные аргументы.
            **options: Передаваемые именованные аргументы.
        """
        print('Importing data from:', settings.DATA_IMPORT_LOCATION)
        with open(
            f'{settings.DATA_IMPORT_LOCATION}/ingredients.csv',
            'r',
            encoding='utf-8-sig',
        ) as csv_file:
            data = csv.reader(csv_file)
            next(data)
            for counter, line in enumerate(data):
                name = line[0]
                measurement_unit = line[1]
                if Ingredient.objects.filter(name=name).exists():
                    obj = Ingredient.objects.get(name=name)
                    obj.measurement_unit = measurement_unit
                    obj.save(
                        update_fields=[
                            'measurement_unit',
                        ],
                    )
                    print(obj)
                else:
                    obj = Ingredient()
                    obj.name = name
                    obj.measurement_unit = measurement_unit
                    obj.save()
                    print(obj)
            print(f'Import complete, imported {counter} products')
