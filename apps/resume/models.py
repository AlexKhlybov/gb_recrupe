import datetime

from dateutil import relativedelta
from django.conf import settings
from django.db import models
from django.db.models import Max, Min


class Resume(models.Model):
    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE,
                             verbose_name='Сотрудник')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    name = models.CharField(max_length=128, db_index=True, verbose_name="Название резюме")
    price = models.IntegerField(db_index=True, null=True, blank=True, verbose_name="Зарплата")
    about_me = models.TextField(max_length=500, null=True, blank=True, verbose_name='Обо мне')

    education = models.ManyToManyField('Education', db_index=True, blank=True, verbose_name='Образование')
    experience = models.ManyToManyField('Experience', db_index=True, blank=True, verbose_name='Опыт работы')
    courses = models.ManyToManyField('Courses', db_index=True, blank=True, verbose_name='Курсы')

    is_draft = models.BooleanField(default=True, db_index=True, verbose_name='Черновик')
    is_active = models.BooleanField(default=False, db_index=True, verbose_name='Активен')

    @property
    def get_experience_text(self):
        experience = self.experience.aggregate(Min('start_date'), Max('end_date'))
        end_date_isnull = self.experience.filter(end_date__isnull=True).count()
        _min: datetime.date = experience['start_date__min'] if experience['start_date__min'] else datetime.date.today()
        _max: datetime.date = experience['end_date__max'] if end_date_isnull == 0 else datetime.date.today()

        diff = relativedelta.relativedelta(_max, _min)
        years = diff.years
        month = diff.months
        days = diff.days

        delta_years = f'{years} {"года" if years < 5 else "лет"}' if years > 1 else f'{years} год'
        delta_month = f'{month} {"месяца" if month < 5 else "месяцев"}' if month > 1 else f'{month} месяц'
        delta_days = f'{days} {"дня" if days < 5 else "дней"}' if days > 1 else f'{days} день'

        if years and month:
            return f'{delta_years} {delta_month}'
        elif years:
            return delta_years
        elif month:
            return delta_month
        elif days:
            return delta_days
        return 'отсутствует'

    def skills(self):
        return ResumeSkills.objects.filter(resume=self)

    @property
    def about_me_lines(self):
        return self.about_me.split('\n')

    def __str__(self):
        return self.name


class ResumeSkills(models.Model):
    class Meta:
        verbose_name = 'Ключевой навык'
        verbose_name_plural = 'Ключевые навыки вакансии'

    resume = models.ForeignKey(Resume, db_index=True, on_delete=models.CASCADE, verbose_name="Резюме")
    name = models.CharField(max_length=32, db_index=True, verbose_name="Навык")

    def __str__(self):
        return f'{self.name} ({self.resume})'


class Experience(models.Model):
    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'
        ordering = ('-start_date', '-end_date')

    start_date = models.DateField(verbose_name='Начало работы')
    end_date = models.DateField(null=True, blank=True, verbose_name='Окончание')  # null - По настоящее время
    organization_name = models.CharField(max_length=128, verbose_name='Организация')
    position = models.CharField(max_length=128, verbose_name='Должность')
    duties = models.TextField(max_length=255, verbose_name='Обязанности на рабочем месте')

    @property
    def duties_lines(self):
        return self.duties.split('\n')

    @property
    def delta_text(self):
        return f'{self.start_date_text} - {self.end_date_text}'

    @property
    def start_date_text(self):
        return f'{self.month_year_to_str(self.start_date)}'

    @property
    def end_date_text(self):
        return f'{self.month_year_to_str(self.end_date)}'

    @property
    def get_experience_text(self):
        diff = relativedelta.relativedelta(self.end_date if self.end_date else datetime.date.today(), self.start_date)
        years = diff.years
        month = diff.months

        delta_years = f'{years} {"года" if years < 5 else "лет"}' if years > 1 else f'{years} год'
        delta_month = f'{month} {"месяца" if month < 5 else "месяцев"}' if month > 1 else f'{month} месяц'

        if years and month:
            return f'{delta_years} {delta_month}'
        elif years:
            return delta_years
        elif month:
            return delta_month
        return 'отсутствует'

    def __str__(self):
        return f'{self.delta_text} {self.organization_name}'

    @staticmethod
    def month_year_to_str(date):
        months = {
            1: 'Январь',
            2: 'Февраль',
            3: 'Март',
            4: 'Апрель',
            5: 'Май',
            6: 'Июнь',
            7: 'Июль',
            8: 'Август',
            9: 'Сентябрь',
            10: 'Октябрь',
            11: 'Ноябрь',
            12: 'Декабрь',
        }
        if date:
            return f'{months[date.month]} {date.year}'
        return 'по настоящее время'


class Education(models.Model):
    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'
        ordering = ('-year_of_ending', )

    LEVEL_SECONDARY = None
    LEVEL_SPECIAL_SECONDARY = 1
    LEVEL_UNFINISHED_HIGHER = 2
    LEVEL_HIGHER = 3
    LEVEL_BACHELOR = 4
    LEVEL_MASTER = 5
    LEVEL_CANDIDATE = 6
    LEVEL_DOCTOR = 7

    LEVEL_VALUES = (
        # (LEVEL_SECONDARY, "Среднее"),
        (LEVEL_SPECIAL_SECONDARY, "Среднее специальное"),
        (LEVEL_UNFINISHED_HIGHER, "Неоконченное высшее"),
        (LEVEL_HIGHER, "Высшее"),
        (LEVEL_BACHELOR, "Бакалавр"),
        (LEVEL_MASTER, "Магистр"),
        (LEVEL_CANDIDATE, "Кандидат наук"),
        (LEVEL_DOCTOR, "Доктор наук"),
    )

    level = models.PositiveSmallIntegerField(choices=LEVEL_VALUES, null=True, blank=True, verbose_name='Уровень')
    educational_institution = models.CharField(max_length=255, verbose_name='Учебное заведение')
    faculty = models.CharField(max_length=255, verbose_name='Факультет')
    specialization = models.CharField(max_length=255, null=True, blank=True, verbose_name='Специализация')
    year_of_ending = models.IntegerField(verbose_name='Год окончания')

    def __str__(self):
        return f'{self.educational_institution} ({self.year_of_ending})'


class Courses(models.Model):
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Повышение квалификации, курсы'

    educational_institution = models.CharField(max_length=255, verbose_name='Учебное заведение')
    faculty = models.CharField(max_length=255, verbose_name='Факультет')
    specialization = models.CharField(max_length=255, null=True, blank=True, verbose_name='Специализация')
    year_of_ending = models.IntegerField(verbose_name='Год окончания')

    def __str__(self):
        return f'{self.educational_institution} ({self.year_of_ending})'


class ResumeModeration(models.Model):
    INDEFINED = "Неизвестно"
    UPPROVE = "Подтверждено"
    BAN = "Запрещено"

    STATUS = (
        (INDEFINED, "Неизвестно"),
        (UPPROVE, "Подтверждено"),
        (BAN, "Запрещено"),
    )

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS,max_length=100, null=True, blank=True, verbose_name='Статус')
    comment = models.TextField(blank=True, verbose_name='Комментрарий модератора')
    date = models.DateField(null=True, blank=True, verbose_name='Время отпраления комментария')

    class Meta:
        verbose_name = 'Модерация резюме '
        verbose_name_plural = 'Модерация резюме'

    def __str__(self):
        return self.resume.name