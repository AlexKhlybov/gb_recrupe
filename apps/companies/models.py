from django.db import models

from apps.users.models import User


class Company(models.Model):
    class Meta:
        verbose_name_plural = 'Company - Организации'

    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    name = models.CharField(max_length=255, db_index=True, verbose_name='Имя организации')
    logo = models.FileField(max_length=64, null=True, verbose_name='Логотип организации')
    url = models.FileField(max_length=64, null=True, verbose_name='Сайт компании')
    city = models.CharField(max_length=64, null=True, db_index=True, verbose_name='Город')
    address = models.CharField(max_length=64, null=True, verbose_name='Адрес организации')
    description = models.TextField(null=True, verbose_name='Описание организации')
    is_active = models.BooleanField(default=False, db_index=True, verbose_name='Активность')

    def __str__(self):
        return f'{self.name}'

    @property
    def short_description(self):
        return ' '.join(self.description.split()[:11]) + '...'
