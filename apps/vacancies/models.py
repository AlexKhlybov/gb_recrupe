from django.db import models

from apps.companies.models import Company


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

    is_closed = models.BooleanField(default=False, db_index=True, verbose_name='Признак снятия вакансии')
    is_active = models.BooleanField(default=False, db_index=True, verbose_name='Активен')

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
    status = models.CharField(choices=STATUS,max_length=100, null=True, blank=True, verbose_name='Статус')
    comment = models.TextField(blank=True, verbose_name='Комментрарий модератора')
    date = models.DateField(null=True, blank=True, verbose_name='Время отпраления комментария')

    class Meta:
        verbose_name = 'Модерация вакансии '
        verbose_name_plural = 'Модерация вакансии'

    def __str__(self):
        return self.vacancy.name