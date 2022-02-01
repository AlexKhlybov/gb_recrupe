from django.db import models

from apps.companies.models import Company
from apps.resume.models import Resume
from apps.vacancies.models import Vacancy


# class CompanyModeration(models.Model):
#     INDEFINED = "Неизвестно"
#     UPPROVE = "Подтверждено"
#     BAN = "Запрещено"
#
#     STATUS = (
#         (INDEFINED, "Неизвестно"),
#         (UPPROVE, "Подтверждено"),
#         (BAN, "Запрещено"),
#     )
#
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     status = models.CharField(choices=STATUS, max_length=100, null=True, blank=True, verbose_name='Статус')
#     comment = models.TextField(blank=True, verbose_name='Комментарий модератора')
#     date = models.DateField(null=True, blank=True, verbose_name='Время отправления комментария')
#
#     class Meta:
#         verbose_name = 'Модерация организаций '
#         verbose_name_plural = 'Модерация организаций'
#
#     def __str__(self):
#         return self.company.name


# class ResumeModeration(models.Model):
#     INDEFINED = "Неизвестно"
#     UPPROVE = "Подтверждено"
#     BAN = "Запрещено"
#
#     STATUS = (
#         (INDEFINED, "Неизвестно"),
#         (UPPROVE, "Подтверждено"),
#         (BAN, "Запрещено"),
#     )
#
#     resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
#     status = models.CharField(choices=STATUS, max_length=100, null=True, blank=True, verbose_name='Статус')
#     comment = models.TextField(blank=True, verbose_name='Комментарий модератора')
#     date = models.DateField(null=True, blank=True, verbose_name='Время отправления комментария')
#
#     class Meta:
#         verbose_name = 'Модерация резюме '
#         verbose_name_plural = 'Модерация резюме'
#
#     def __str__(self):
#         return self.resume.name
#
#
# class VacancyModeration(models.Model):
#     INDEFINED = "Неизвестно"
#     UPPROVE = "Подтверждено"
#     BAN = "Запрещено"
#
#     STATUS = (
#         (INDEFINED, "Неизвестно"),
#         (UPPROVE, "Подтверждено"),
#         (BAN, "Запрещено"),
#     )
#
#     vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
#     status = models.CharField(choices=STATUS, max_length=100, null=True, blank=True, verbose_name='Статус')
#     comment = models.TextField(blank=True, verbose_name='Комментарий модератора')
#     date = models.DateField(null=True, blank=True, verbose_name='Время отправления комментария')
#
#     class Meta:
#         verbose_name = 'Модерация вакансии '
#         verbose_name_plural = 'Модерация вакансии'
#
#     def __str__(self):
#         return self.vacancy.name
