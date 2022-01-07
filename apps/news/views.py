from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.news.models import News


class NewsListView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.all()


class NewsDetailView(DetailView):
    model = News
