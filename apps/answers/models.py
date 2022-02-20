from django.db import models
from apps.users.models import User
from apps.vacancies.models import Vacancy
from apps.resume.models import Resume
from apps.companies.models import Company


# Create your models here.

class VacancyAnswers(models.Model):
    STATUS = (
        (1, 'Отправлено'),
        (2, 'Принято'),
        (3, 'Отклонено'),
    )

    user = models.ForeignKey(User, related_name="emoloyee_answer", verbose_name='Соискатель', on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, related_name="answers_vacancy", verbose_name='Вакансия',
                                on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, related_name="attached_resume", verbose_name='Прикрепленное резюме',
                               on_delete=models.CASCADE)

    message = models.CharField(max_length=1500, blank=True, verbose_name='Сообщение от соискателя')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    status = models.IntegerField(choices=STATUS, db_index=True, default=1, verbose_name='Статус')

    class Meta:
        verbose_name = 'Ответ на вакансию'
        verbose_name_plural = 'Ответы на вакансии'

    def __str__(self):
        return f'{self.vacancy.name} ({self.user.get_full_name}) ({self.resume.name}) ({self.message})'

    @staticmethod
    def get_number_employee_answers(user):
        return VacancyAnswers.objects.filter(user=user).count()

    @staticmethod
    def get_number_company_answers(company):
        return VacancyAnswers.get_company_answers(company).count()

    @staticmethod
    def get_employee_answers(user):
        return VacancyAnswers.objects.filter(user=user)

    @staticmethod
    def get_company_answers(company):
        print(f'company: {company}')
        vacancies_id = [vacancies.id for vacancies in Vacancy.objects.filter(company=company)]
        final_set = VacancyAnswers.objects.none()
        for i in range(len(vacancies_id)):
            final_set = final_set | VacancyAnswers.objects.filter(vacancy=vacancies_id[i])

        return final_set


class ResumeAnswers(models.Model):
    STATUS = (
        (1, 'Отправлено'),
        (2, 'Принято'),
        (3, 'Отклонено'),
    )

    user = models.ForeignKey(User, related_name="company_answer", verbose_name='Компания', on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, related_name="answers_resume", verbose_name='Резюме',
                               on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, related_name="attached_vacancy", verbose_name='Прикрепленная вакансия',
                                on_delete=models.CASCADE)

    message = models.CharField(max_length=1500, blank=True, verbose_name='Сообщение от компании')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    status = models.IntegerField(choices=STATUS, db_index=True, default=1, verbose_name='Статус')

    class Meta:
        verbose_name = 'Предложение о работе'
        verbose_name_plural = 'Предложения о работе'

    def __str__(self):
        return f'{self.resume.name} ({self.user.get_full_name}) ({self.vacancy.name}) ({self.message})'

    @staticmethod
    def get_number_employee_resume_answer(user):
        return ResumeAnswers.get_employee_resume_answers(user).count()

    @staticmethod
    def get_number_company_resume_answers(user):
        return ResumeAnswers.objects.filter(user=user).count()

    @staticmethod
    def get_employee_resume_answers(user):
        resumes_id = [resume.id for resume in Resume.objects.filter(user=user)]
        final_set = ResumeAnswers.objects.none()
        for i in range(len(resumes_id)):
            final_set = final_set | ResumeAnswers.objects.filter(resume=resumes_id[i])

        return final_set

    @staticmethod
    def get_company_resume_answers(user):
        return ResumeAnswers.objects.filter(user=user)
