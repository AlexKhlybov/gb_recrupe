from django.contrib import admin
from import_export import resources

from apps.vacancies.models import Vacancy, VacancyModeration, VacancySkills

admin.site.register(Vacancy)
admin.site.register(VacancyModeration)


class VacancyResource(resources.ModelResource):
    class Meta:
        model = Vacancy


class VacancySkillsResource(resources.ModelResource):
    class Meta:
        model = VacancySkills
        exclude = ('id', )

class VacancyModerationResource(resources.ModelResource):
    class Meta:
        model = VacancyModeration