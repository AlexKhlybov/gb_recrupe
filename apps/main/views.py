
from django.shortcuts import render

from apps.companies.models import Company
from apps.news.models import News

from django.views.generic import CreateView, DeleteView, ListView, UpdateView


class HomePageList(ListView):
    model = News
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news"] = News.objects.all()[:2]
        context["partners"] = Company.objects.filter(is_active=True)[:10]
        context["title"] = "Recrupe | Главная"
        return context


def specification(request):
    return render(request, 'main/specification.html')


def posting_rules(request):
    return render(request, 'main/posting_rules.html')
