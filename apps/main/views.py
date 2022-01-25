
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.companies.models import Company
from apps.news.models import News
from apps.resume.models import Resume, ResumeFavorites
from apps.vacancies.models import Vacancy, VacancyFavorites


class HomePageList(ListView):
    model = News
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Recrupe | Главная"
        context["news"] = News.objects.all()[:2]
        context["partners"] = Company.objects.filter(is_active=True)[:10]
        context["job_recomendations"] = Vacancy.objects.filter(is_active=True)[:5]
        context["resume_recomendations"] = Resume.objects.filter(is_active=True)[:5]
        # if self.request.user.role == 2:
        #     context["favorite"] = VacancyFavorites.get_favorite_vacancy_from_user(self.request.user.id)
        # if self.request.user.role == 3:
        #     context["favorite"] = ResumeFavorites.get_favorite_resume_from_user(self.request.user.id)
        return context


def specification(request):
    return render(request, 'main/specification.html')


def posting_rules(request):
    return render(request, 'main/posting_rules.html')
