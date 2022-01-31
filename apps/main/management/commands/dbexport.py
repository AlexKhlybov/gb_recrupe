import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from apps.companies.admin import CompanyResource
from apps.main.admin import CityResource
from apps.news.admin import NewsResource
from apps.resume.admin import (CoursesResource, EducationResource,
                               ExperienceResource, ResumeResource,
                               ResumeSkillsResource)
from apps.users.admin import UserResource
from apps.vacancies.admin import VacancyResource, VacancySkillsResource
from apps.notify.admin import NotifyTemplateResource, SMTPAccountResource


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-m', '--models', nargs='+', type=str, default=[])

    def handle(self, *args, **options):
        resource = [CityResource, UserResource, NewsResource]
        resource += [CompanyResource, VacancyResource, VacancySkillsResource]
        resource += [EducationResource, ExperienceResource, CoursesResource, ResumeResource, ResumeSkillsResource]
        resource += [SMTPAccountResource, NotifyTemplateResource]

        for i in resource:
            self.export_model(i, options)

    @staticmethod
    def export_model(resource_class, options):
        assert resource_class.__name__[-8:] == 'Resource'
        name = resource_class.__name__[:-8]
        full_file_name = os.path.join(settings.BASE_DIR, 'apps', 'main', 'management', 'json', f'{name}.json')
        if options.get('models') and name.lower() not in options.get('models', []):
            return

        dataset = resource_class().export()
        data = json.loads(dataset.json)
        print(f'export {name}... ', end='', flush=True)
        with open(full_file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print('OK', f'exported {len(data)} rows')
