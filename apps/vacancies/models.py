from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import Q

from apps.companies.models import Company
from apps.users.models import User


class VacancyPublicManager(models.Manager):
    def get_queryset(self):
        """
        Объектный менеджер, показывающий только активные вакансии, и те на которые отправили жалобу.
        С публикации снимаем черновики и те, на которые модератор отправил претензию (подтвердил жалобу)
        """
        return super().get_queryset().filter(Q(status=Vacancy.STATUS_PUBLIC) | Q(status=Vacancy.STATUS_COMPLAINT))


class Vacancy(models.Model):
    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Вакансии'

    # STATUS_DRAFT = 1
    STATUS_PUBLIC = 2
    STATUS_COMPLAINT = 3
    STATUS_CLAIM = 4

    STATUS = (
        # (STATUS_DRAFT, 'Черновик'),
        (STATUS_PUBLIC, 'Опубликовано'),
        (STATUS_COMPLAINT, 'Жалоба'),
        (STATUS_CLAIM, 'Заблокировано'),
    )

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
    description = RichTextField(max_length=5000, verbose_name='Описание вакансии')
    experience = models.PositiveSmallIntegerField(choices=EXPERIENCE, db_index=True, default=EXPERIENCE_NONE,
                                                  verbose_name="Опыт работы")
    price_min = models.IntegerField(verbose_name="Зарплата от", db_index=True, null=True, blank=True)
    price_max = models.IntegerField(verbose_name="Зарплата до", db_index=True, null=True, blank=True)
    favorites = models.ManyToManyField(User, related_name="favorites_vacancy", through="VacancyFavorites",
                                       through_fields=("vacancy", "user"))
    # answers = models.ManyToManyField(User, related_name="answers_vacancy", through="VacancyAnswers",
    #                                    through_fields=("vacancy", "user"))
    status = models.IntegerField(choices=STATUS, db_index=True, default=STATUS_PUBLIC, verbose_name='Статус')

    objects = models.Manager()
    public = VacancyPublicManager()

    def __str__(self):
        return f"{self.name}"

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

    def get_answer_resume(self):
        """ Возвращает все отклики на вакансию """
        from apps.answers.models import VacancyAnswers
        return [x.resume_id for x in VacancyAnswers.objects.filter(vacancy=self)]

    def delete(self, using=None, keep_parents=False):
        VacancySkills.objects.filter(vacancy=self).delete()
        super().delete(using, keep_parents)
    
    @staticmethod
    def get_complaint():
        return Vacancy.objects.filter(status=3).count()


class VacancySkills(models.Model):
    class Meta:
        verbose_name_plural = 'Ключевые навыки вакансии'

    vacancy = models.ForeignKey(Vacancy, db_index=True, on_delete=models.CASCADE, verbose_name="Вакансия")
    name = models.CharField(max_length=32, db_index=True, verbose_name="Навык")

    def __str__(self):
        return f'{self.name} ({self.vacancy})'


class VacancyFavorites(models.Model):
    user = models.ForeignKey(User, related_name="my_favor_vacancy", verbose_name='Соискатель', on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, related_name="favorites_vacancy", verbose_name='Вакансия',
                                on_delete=models.CASCADE)
    
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
        return VacancyFavorites.objects.filter(user_id=user_id).values_list('vacancy', flat=True).order_by('id')
    
    @classmethod
    def get_number_favorite(cls, user):
        return VacancyFavorites.objects.filter(user=user).count()
