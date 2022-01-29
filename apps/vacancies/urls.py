from django.urls import re_path, path

from apps.vacancies import views as vacancies

app_name = 'vacancies'

urlpatterns = [
    path('', vacancies.VacancyListView.as_view(), name='all'),
    path('<int:pk>/', vacancies.VacancyDetailView.as_view(), name='detail'),
    path('create/', vacancies.create, name="create"),
    path('edit/<int:pk>/', vacancies.edit, name="edit"),
    path('my/', vacancies.MyVacancyCompanyListView.as_view(), name='my'),

    re_path(r'^favorites/(?P<pk>\d+)/', vacancies.FavoritesVacancyListView.as_view(), name='favorites'),
    re_path(r'^edit-favorites/(?P<vacancy>\d+)/$', vacancies.favorites_edit, name='favorites-edit'),
]
