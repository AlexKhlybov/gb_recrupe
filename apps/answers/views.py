from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from apps.resume.models import Resume
from apps.answers.models import VacancyAnswers, ResumeAnswers
from apps.users.models import User
from apps.vacancies.models import Vacancy
from apps.companies.models import Company


class EmployeeAnswersListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = "answers/my_answers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Recrupe | Мои отклики"
        context["my_answers"] = VacancyAnswers.get_employee_answers(self.request.user.id)
        # context["my_answers_count"] = VacancyAnswers.get_number_employee_answers(self.request.user.id)
        return context


class EmployeeOffersListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = "answers/my_offers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Recrupe | Предложения о работе"
        context["my_offers"] = ResumeAnswers.get_employee_resume_answers(self.request.user.id)
        context["my_offers_count"] = ResumeAnswers.get_number_employee_resume_answer(self.request.user.id)
        return context


class CompanyOffersListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = "answers/offers_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Recrupe | Мои предложения"
        context["company_offers"] = ResumeAnswers.get_company_resume_answers(self.request.user.id)
        context["company_offers_count"] = ResumeAnswers.get_number_company_resume_answers(self.request.user.id)
        return context


class CompanyAnswersListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = "answers/answers_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Recrupe | Отклики на предложения нашей компании"
        if len(Company.objects.filter(user=self.request.user.id)):
            context["company_answers"] = VacancyAnswers.get_company_answers(Company.objects.get(user=self.request.user))
        else:
            context["company_answers"] = VacancyAnswers.objects.none()
        return context


def vacancy_answer(request, vacancy_id, resume_id):
    user = User.objects.get(id=request.user.id)
    resume = get_object_or_404(Resume, pk=resume_id)
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    obj, created = VacancyAnswers.objects.get_or_create(user=user, resume=resume, vacancy=vacancy, message="")
    if not created:
        obj.delete()
    return JsonResponse({"delete": not created}, status=200)


def resume_answer(request, resume_id, vacancy_id):
    user = User.objects.get(id=request.user.id)
    resume = get_object_or_404(Resume, pk=resume_id)
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    obj, created = ResumeAnswers.objects.get_or_create(user=user, resume=resume, vacancy=vacancy, message="")
    if not created:
        obj.delete()
    return JsonResponse({"delete": not created}, status=200)


def vacancy_answer_edit_temp(request, resume_name, vacancy):
    user = User.objects.get(id=request.user.id)
    resume = Resume.objects.get(name=resume_name)
    vacancy = Vacancy.objects.get(id=vacancy)
    obj, created = VacancyAnswers.objects.get_or_create(user=user, resume=resume, vacancy=vacancy, message="")
    if not created:
        obj.delete()
    return JsonResponse({"delete": not created}, status=200)
