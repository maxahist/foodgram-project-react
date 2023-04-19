import csv

from django.core.management.base import BaseCommand

from food.models import Food


class Command(BaseCommand):
    help = '''Загрузка информации из csv-файла в базу данных.'''

    def handle(self, *args, **options):
        with open('data/ingredients.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, measurement_unit = row
                Food.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )