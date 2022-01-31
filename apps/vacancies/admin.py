from django.contrib import admin
from import_export import resources

from apps.vacancies.models import Vacancy, VacancySkills

admin.site.register(Vacancy)


class VacancyResource(resources.ModelResource):
    class Meta:
        model = Vacancy


class VacancySkillsResource(resources.ModelResource):
    class Meta:
        model = VacancySkills
        exclude = ('id', )
