import datetime

from dateutil import relativedelta
from django.conf import settings
from django.db import models
from django.db.models import Max, Min, Q

from apps.users.models import User


class ResumePublicManager(models.Manager):
    def get_queryset(self):
        """
        Объектный менеджер, показывающий только активные резюме, и те на которые отправили жалобу.
        С публикации снимаем черновики и те, на которые модератор отправил претензию (подтвердил жалобу)
        """
        return super().get_queryset().filter(Q(status=Resume.STATUS_PUBLIC) | Q(status=Resume.STATUS_COMPLAINT))


class Resume(models.Model):
    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering = ('-updated_at', '-id', )

    STATUS_DRAFT = 1
    STATUS_PUBLIC = 2
    STATUS_COMPLAINT = 3
    STATUS_CLAIM = 4

    STATUS = (
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PUBLIC, 'Опубликовано'),
        (STATUS_COMPLAINT, 'Жалоба'),
        (STATUS_CLAIM, 'Претензия'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE,
                             verbose_name='Соискатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    name = models.CharField(max_length=128, db_index=True, verbose_name="Название резюме")
    price = models.IntegerField(db_index=True, null=True, blank=True, verbose_name="Зарплата")
    about_me = models.TextField(max_length=500, null=True, blank=True, verbose_name='О себе')

    education = models.ManyToManyField('Education', db_index=True, blank=True, verbose_name='Образование')
    experience = models.ManyToManyField('Experience', db_index=True, blank=True, verbose_name='Опыт работы')
    courses = models.ManyToManyField('Courses', db_index=True, blank=True, verbose_name='Курсы')
    favorites = models.ManyToManyField(User, related_name="favorites_resume", through="ResumeFavorites",
                                       through_fields=("resume", "user"))
    # answers = models.ManyToManyField(User, related_name="answers_resume", through="ResumeAnswers",
    #                                  through_fields=("resume", "user"))
    status = models.IntegerField(choices=STATUS, db_index=True, default=STATUS_PUBLIC, verbose_name='Статус')

    objects = models.Manager()
    public = ResumePublicManager()

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

    @property
    def get_experience_year(self):
        experience = self.experience.aggregate(Min('start_date'), Max('end_date'))
        end_date_isnull = self.experience.filter(end_date__isnull=True).count()
        _min: datetime.date = experience['start_date__min'] if experience['start_date__min'] else datetime.date.today()
        _max: datetime.date = experience['end_date__max'] if end_date_isnull == 0 else datetime.date.today()

        diff = relativedelta.relativedelta(_max, _min)
        years = diff.years
        month = diff.months

        return years + month/12

    @property
    def skills(self):
        return ResumeSkills.objects.filter(resume=self)
    
    @staticmethod
    def get_favorite_resume(user):
        """Возвращает через пользователя (м2м) все избранные им резюме"""
        user = User.objects.get(id=user)
        return user.favorites_resume.all()

    @property
    def about_me_lines(self):
        return self.about_me.split('\n')

    def delete(self, using=None, keep_parents=False):
        ResumeSkills.objects.filter(resume=self).delete()
        super().delete(using, keep_parents)

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


class ResumeFavorites(models.Model):
    user = models.ForeignKey(User, related_name="my_response", verbose_name='Работодатель',
                             on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, related_name="favorites_resume",  verbose_name='Резюме',
                               on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    
    class Meta:
        verbose_name = 'Избранное резюме'
        verbose_name_plural = 'Избранные резюме'
    
    def __str__(self):
        return f'{self.resume.name} ({self.user.get_full_name})'
    
    @classmethod
    def get_number_favorite(cls, user):
        return ResumeFavorites.objects.filter(user=user).count()
    
    @staticmethod
    def get_favorite_resume_from_user(user_id):
        return ResumeFavorites.objects.filter(user=user_id)
    
    @staticmethod
    def get_favorite_vacancy_list(user_id):
        """Возвращает список id вакансий добавленных в избранное"""
        return ResumeFavorites.objects.filter(user_id=user_id).values_list('resume', flat=True).order_by('id')
