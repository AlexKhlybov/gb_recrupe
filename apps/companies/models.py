from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.main.models import City
from apps.tools import upload_to_and_rename
from apps.users.models import User


class CompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Company.STATUS_PUBLIC)


class Company(models.Model):
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    STATUS_MODERATION = 1
    STATUS_REFUSAL = 2
    STATUS_PUBLIC = 3

    STATUS = (
        (STATUS_MODERATION, 'На модерации'),
        (STATUS_REFUSAL, 'Отказ в публикации'),
        (STATUS_PUBLIC, 'Опубликовано'),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    name = models.CharField(max_length=255, db_index=True, verbose_name='Имя организации', blank=True)
    logo = models.FileField(max_length=64, null=True, verbose_name='Логотип организации', blank=True,
                            upload_to=upload_to_and_rename('companies', 'logo'))
    url = models.URLField(max_length=64, null=True, verbose_name='Сайт компании', blank=True)
    city = models.ForeignKey(City, null=True, db_index=True, verbose_name='Город', blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=64, null=True, verbose_name='Адрес организации', blank=True)
    description = models.TextField(max_length=5000, null=True, verbose_name='Описание организации', blank=True)
    status = models.IntegerField(choices=STATUS, db_index=True, default=STATUS_MODERATION, verbose_name='Статус')

    @receiver(post_save, sender=User)
    def create_company_profile(sender, instance, created, **kwargs):
        if created:
            if instance.role == 3:
                Company.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_company_profile(sender, instance, **kwargs):
        if instance.role == 3:
            instance.company.save()

    objects = models.Manager()
    public = CompanyManager()

    def vacancy_count(self):
        """
        Количество активных вакансий
        """
        from apps.vacancies.models import Vacancy
        return Vacancy.public.filter(company=self).count()

    def __str__(self):
        return self.name

    @property
    def short_description(self):
        return ' '.join(self.description.split()[:11]) + '...'

    def split_description_to_lines(self):
        return self.description.split('\n')
