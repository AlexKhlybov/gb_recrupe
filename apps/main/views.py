
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
        context["partners"] = Company.public.all()[:10]
        context["job_recomendations"] = Vacancy.public.all()[:10]
        context["resume_recomendations"] = Resume.public.filter()[:10]
        return context


def specification(request):
    return render(request, 'main/specification.html')


def posting_rules(request):
    return render(request, 'main/posting_rules.html')
