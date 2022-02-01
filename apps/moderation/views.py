from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.companies.models import Company
from apps.resume.models import Resume
from apps.vacancies.models import Vacancy


class CompanyModerationUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    fields = ['status', 'comment']
    template_name = 'moderation/company_moderation.html'
    success_url = reverse_lazy('companies:')


@login_required
def company_moderation(request):
    if request.GET.get('find'):
        company_list = Company.objects.filter(
            Q(name__icontains=request.GET.get('find'))
        )
    else:
        company_list = Company.objects.filter(status=Company.STATUS_MODERATION)

    content = {
        'company_list': company_list,
        'title': 'Модерация'
    }
    return render(request, 'moderation/company_list_moderation.html', content)


@login_required
def vacancy_moderation(request):
    if request.GET.get('find'):
        vacancy_list = Vacancy.objects.filter(name__icontains=request.GET.get('find'))
    else:
        vacancy_list = Vacancy.objects.all()
    content = {
        'vacancy_list': vacancy_list.filter(status=Resume.STATUS_COMPLAINT),
        'title': 'Модерация вакансии'
    }
    return render(request, 'moderation/vacancy_list_moderation.html', content)


# class VacancyModerationUpdateView(UpdateView):
#     model = VacancyModeration
#     fields = ['status', 'comment']
#     template_name = 'moderation/vacancy_moderation.html'
#     success_url = reverse_lazy('vacancies:moderation-vacancy')


@login_required
def resume_moderation(request):
    if request.GET.get('find'):
        resume_list = Resume.objects.filter(status=Resume.STATUS_COMPLAINT, name__icontains=request.GET.get('find'))
    else:
        resume_list = Resume.objects.filter(status=Resume.STATUS_COMPLAINT)
    content = {
        'resume_list': resume_list,
        'title': 'Модерация резюме'
    }
    return render(request, 'moderation/resume_list_moderation.html', content)
