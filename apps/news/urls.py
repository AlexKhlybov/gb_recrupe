from django.urls import path

from apps.news import views as news

app_name = 'users'

urlpatterns = [
    path('', news.NewsListView.as_view(), name='all'),
    path('<int:pk>/', news.NewsDetailView.as_view(), name='detail_news'),
]
