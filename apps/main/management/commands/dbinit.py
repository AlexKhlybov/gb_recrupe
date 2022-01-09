import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from apps.companies.models import Company
from apps.news.models import News
from apps.users.models import User


def load_from_json(file_name):
    full_file_name = os.path.join(settings.BASE_DIR, 'apps', 'main', 'management', 'json', f'{file_name}.json')
    with open(full_file_name, 'r', encoding='utf-8') as f:
        return json.load(f, )


def insert_to_model(model):
    json_name = model.__name__
    json_data = load_from_json(json_name)
    print(f'insert from {json_name}... ', end='')
    if model.objects.all().count() == 0:
        for item in json_data:
            if model.__name__ == User.__name__:
                User.objects.create_user(**item)
            else:
                model.objects.create(**item)

        print('OK', f'inserted {len(json_data)} rows')
    else:
        print('ERROR', 'table not empty')


class Command(BaseCommand):
    def handle(self, *args, **options):
        insert_to_model(User)
        insert_to_model(News)
        insert_to_model(Company)
