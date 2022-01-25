from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User


class CompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Company(models.Model):
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    # user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    name = models.CharField(max_length=255, db_index=True, verbose_name='Имя организации', blank=True)
    logo = models.FileField(max_length=64, null=True, verbose_name='Логотип организации', blank=True)
    url = models.URLField(max_length=64, null=True, verbose_name='Сайт компании', blank=True)
    city = models.CharField(max_length=64, null=True, db_index=True, verbose_name='Город', blank=True)
    address = models.CharField(max_length=64, null=True, verbose_name='Адрес организации', blank=True)
    description = models.TextField(max_length=5000, null=True, verbose_name='Описание организации', blank=True)
    is_active = models.BooleanField(default=False, db_index=True, verbose_name='Активность')

    @receiver(post_save, sender=User)
    def create_company_profile(sender, instance, created, **kwargs):
        if created:
            if instance.role == 3:
                Company.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_company_profile(sender, instance, **kwargs):
        if instance.role == 3:
            # print(f'instance: {instance.company}')
            instance.company.save()

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
    status = models.CharField(choices=STATUS, max_length=100, null=True, blank=True, verbose_name='Статус')
    comment = models.TextField(blank=True, verbose_name='Комментарий модератора')
    date = models.DateField(null=True, blank=True, verbose_name='Время отправления комментария')

    class Meta:
        verbose_name = 'Модерация организаций '
        verbose_name_plural = 'Модерация организаций'

    def __str__(self):
        return self.company.name
