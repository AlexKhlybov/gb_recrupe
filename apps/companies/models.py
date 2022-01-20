from django.db import models

from apps.users.models import User


class CompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Company(models.Model):
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    name = models.CharField(max_length=255, db_index=True, verbose_name='Имя организации')
    logo = models.FileField(max_length=64, null=True, verbose_name='Логотип организации')
    url = models.URLField(max_length=64, null=True, verbose_name='Сайт компании')
    city = models.CharField(max_length=64, null=True, db_index=True, verbose_name='Город')
    address = models.CharField(max_length=64, null=True, verbose_name='Адрес организации')
    description = models.TextField(max_length=5000, null=True, verbose_name='Описание организации')
    is_active = models.BooleanField(default=False, db_index=True, verbose_name='Активность')

    # objects = CompanyManager()

    def vacancy_count(self):
        """
        Количество активных вакансий
        """
        from apps.vacancies.models import Vacancy
        return Vacancy.objects.filter(company=self, is_closed=False, is_active=True).count()

    def __str__(self):
        return self.name

    @property
    def short_description(self):
        return ' '.join(self.description.split()[:11]) + '...'

    def split_description_to_lines(self):
        return self.description.split('\n')


class CompanyModeration(models.Model):
    INDEFINED = "Неизвестно"
    UPPROVE = "Подтверждено"
    BAN = "Запрещено"

    STATUS = (
        (INDEFINED, "Неизвестно"),
        (UPPROVE, "Подтверждено"),
        (BAN, "Запрещено"),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS,max_length=100, null=True, blank=True, verbose_name='Статус')
    comment = models.TextField(blank=True, verbose_name='Комментрарий модератора')
    date = models.DateField(null=True, blank=True, verbose_name='Время отпраления комментария')

    class Meta:
        verbose_name = 'Модерация организаций '
        verbose_name_plural = 'Модерация организаций'

    def __str__(self):
        return self.company.name