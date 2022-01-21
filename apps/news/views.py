from django.views.generic import DetailView, ListView

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
