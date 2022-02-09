from operator import mod
from django.db import models
from solo.models import SingletonModel


class City(models.Model):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    region = models.CharField(max_length=64, null=False, db_index=True, verbose_name='Регион')
    city = models.CharField(max_length=32, null=False, db_index=True, verbose_name='Город')


    def __str__(self):
        return self.city


class SiteConfiguration(SingletonModel):
    logo = models.ImageField(
        verbose_name="Логотип",
        upload_to="Изображение",
        default="logo.png",
        help_text="Логотип сайта",
    )
    name = models.CharField(verbose_name="Название", max_length=128, help_text="УК Новый город")
    tagline = models.CharField(verbose_name="Слоган", max_length=128, help_text="Работа найдется для каждого")
    city = models.CharField(verbose_name="Город", max_length=128, help_text="Москва")
    street = models.CharField(verbose_name="Улица", max_length=256, help_text="ул.Свободы")
    num_building = models.CharField(verbose_name="Номер здания", max_length=5, help_text="д.5")
    phone = models.CharField(
        verbose_name="Телефон", max_length=11, null=True, blank=True, help_text="Номер телефона в формате - 79823212334"
    )
    email = models.EmailField(verbose_name="e-mail", help_text="info@uk.ru")
    site = models.CharField(verbose_name="Сайт", max_length=128, help_text="www.uk-newcity.ru")

    key_ya = models.CharField(
        verbose_name="Api-ключ Яндекса", max_length=128, blank=True, help_text="1888f9f3-1174-48c4-b1b4-fa129bй2345234"
    )
    lat = models.CharField(verbose_name="Широта", max_length=64, blank=True, help_text="57.167979")
    lon = models.CharField(verbose_name="Долгота", max_length=64, blank=True, help_text="65.564430")

    footer_copyright = models.CharField(
        max_length=256, blank=True, default="Все права защищены © Москва 2021 - 2022 гг.", verbose_name="Футер копирайт"
    )
    dev_info = models.CharField(max_length=128, default="Команда №4", verbose_name="Информация о разработчиках сайта")
    
    vk = models.CharField(max_length=128, default="https://vk.com/", verbose_name="Страница ВКонтакте")
    im = models.CharField(max_length=128, default="https://instagram.com/", verbose_name="Страница Instagram")
    fb = models.CharField(max_length=128, default="https://facebook.com/", verbose_name="Страница Facebook")
    tw = models.CharField(max_length=128, default="https://twitter.com/", verbose_name="Страница Twitter")


    def get_absolute_url(self):
        return f"/media/{self.logo}"

    def __str__(self):
        return "Настройки сайта"

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
    
    def get_site(self):
        return f'{self.site}'

    class Meta:
        verbose_name = "Настройки сайта"
