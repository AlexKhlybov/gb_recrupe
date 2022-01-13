from django.urls import path

from apps.vacancies import views as vacancies

app_name = 'vacancies'

urlpatterns = [
    path('', vacancies.VacancyListView.as_view(), name='all'),
    path('<int:pk>/', vacancies.VacancyDetailView.as_view(), name='detail'),
]
