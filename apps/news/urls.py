from django.urls import path

from apps.news import views as news

app_name = 'news'

urlpatterns = [
    path('', news.NewsListView.as_view(), name='all'),
    path('<int:pk>/', news.NewsDetailView.as_view(), name='detail_news'),
    path('create/', news.NewsCreateView.as_view(), name='create_news'),
    path('update/<int:pk>/', news.NewsUpdateView.as_view(), name='update_news'),
]
