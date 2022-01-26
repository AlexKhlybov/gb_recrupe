from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from pyexpat import model

from apps.news.forms import NewsEditForm
from apps.news.models import News


class NewsListView(ListView):
    model = News
    template_name = "news/news_list.html"

    def get_queryset(self):
        return News.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список новостей"
        return context


class NewsDetailView(DetailView):
    model = News
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Детали новости"
        return context
    

class NewsUpdateView(UpdateView):
    model = News
    success_url = reverse_lazy("news:all")
    form_class = NewsEditForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новость/редактирование"
        context["page_name"] = "Редактирование новости"
        return context
    

class NewsCreateView(CreateView):
    model = News
    success_url = reverse_lazy("news:all")
    form_class = NewsEditForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новость/создание"
        context["page_name"] = "Создание новости"
        return context
