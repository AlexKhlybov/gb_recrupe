from django.db import models


class City(models.Model):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    region = models.CharField(max_length=64, null=False, db_index=True, verbose_name='Регион')
    city = models.CharField(max_length=32, null=False, db_index=True, verbose_name='Город')
