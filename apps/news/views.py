from django.views.generic import DetailView, ListView

from apps.news.models import News


class NewsListView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.all()


class NewsDetailView(DetailView):
    model = News
