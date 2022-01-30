from ast import mod

from django.db import models

from apps.companies.models import Company
from apps.users.models import User


class Vacancy(models.Model):
    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Вакансии'

    EXPERIENCE_NONE = 1
    EXPERIENCE_1_3 = 2
    EXPERIENCE_3_6 = 3
    EXPERIENCE_6 = 4

    EXPERIENCE = (
        (EXPERIENCE_NONE, 'Не имеет значения'),
        (EXPERIENCE_1_3, 'от 1 года до 3 лет'),
        (EXPERIENCE_3_6, 'от 3 до 6 лет'),
        (EXPERIENCE_6, 'более 6 лет'),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancy_company',
                                verbose_name='Компания')
    name = models.CharField(max_length=128, db_index=True, verbose_name="Название вакансии")
    description = models.TextField(max_length=5000, verbose_name='Описание вакансии')
    experience = models.PositiveSmallIntegerField(choices=EXPERIENCE, db_index=True, default=EXPERIENCE_NONE,
                                                  verbose_name="Опыт работы")
    price_min = models.IntegerField(verbose_name="Зарплата от", db_index=True, null=True, blank=True)
    price_max = models.IntegerField(verbose_name="Зарплата до", db_index=True, null=True, blank=True)
    # skills = models.ManyToManyField(VacancySkills)
    
    favorites = models.ManyToManyField(User, related_name="favorites_vacancy", through="VacancyFavorites", through_fields=("vacancy", "user"))

    is_closed = models.BooleanField(default=False, db_index=True, verbose_name='Признак снятия вакансии')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Активен')

    @property
    def split_description_to_lines(self):
        return self.description.split('\n')

    @property
    def price(self):
        value = f'от {self.price_min}' if self.price_min else ''
        if self.price_max:
            value += ' ' if value else ''
            value += f'до {self.price_max}'
        if value:
            value += ' руб.'

        return value if value else 'з/п не указана'

    @property
    def skills(self):
        return VacancySkills.objects.filter(vacancy=self)
    
    @staticmethod
    def get_favorite_vacancy(user):
        """Возвращает через пользователя (м2м) все избранные им вакансии"""
        user = User.objects.get(id=user)
        return user.favorites_vacancy.all()
    

    def delete(self, using=None, keep_parents=False):
        VacancySkills.objects.filter(vacancy=self).delete()
        super().delete(using, keep_parents)


    def __str__(self):
        return f"{self.name}"


class VacancySkills(models.Model):
    class Meta:
        verbose_name_plural = 'Ключевые навыки вакансии'

    vacancy = models.ForeignKey(Vacancy, db_index=True, on_delete=models.CASCADE, verbose_name="Вакансия")
    name = models.CharField(max_length=32, db_index=True, verbose_name="Навык")

    def __str__(self):
        return f'{self.name} ({self.vacancy})'

class VacancyModeration(models.Model):
    INDEFINED = "Неизвестно"
    UPPROVE = "Подтверждено"
    BAN = "Запрещено"

    STATUS = (
        (INDEFINED, "Неизвестно"),
        (UPPROVE, "Подтверждено"),
        (BAN, "Запрещено"),
    )

    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=100, null=True, blank=True, verbose_name='Статус')
    comment = models.TextField(blank=True, verbose_name='Комментрарий модератора')
    date = models.DateField(null=True, blank=True, verbose_name='Время отпраления комментария')

    class Meta:
        verbose_name = 'Модерация вакансии '
        verbose_name_plural = 'Модерация вакансии'

    def __str__(self):
        return self.vacancy.name

      
class VacancyFavorites(models.Model):
    user = models.ForeignKey(User, related_name="my_favor_vacancy", verbose_name='Соискатель', on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, related_name="favorites_vacancy", verbose_name='Вакансия', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    
    class Meta:
        verbose_name = 'Избранная вакансия'
        verbose_name_plural = 'Избранные вакансии'
    
    def __str__(self):
        return f'{self.vacancy.name} ({self.user.get_full_name})'

    @staticmethod
    def get_favorite_vacancy_from_user(user_id):
        return VacancyFavorites.objects.filter(user=user_id)
    
    @staticmethod
    def get_favorite_vacancy_list(user_id):
        """Возвращает список id вакансий добавленных в избранное"""
        # TODO сделать фильтрацию под юзера
        return VacancyFavorites.objects.values_list('vacancy', flat=True).order_by('id')
    
    @classmethod
    def get_number_favorite(cls, user):
        return VacancyFavorites.objects.filter(user=user).count()
