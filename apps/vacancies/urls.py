from django.urls import path

from apps.vacancies import views as vacancies

app_name = 'vacancies'

urlpatterns = [
    path('', vacancies.VacancyListView.as_view(), name='all'),
    path('create/', vacancies.create, name='create'),
    path('edit/<int:pk>/', vacancies.edit, name='edit'),
    path('<int:pk>/', vacancies.VacancyDetailView.as_view(), name='detail'),
    path('moderation-vacancy/', vacancies.vacancy_moderation, name='moderation-vacancy'),
    path('<int:pk>/moderation-vacancy/', vacancies.VacancyModarationUpdateView.as_view(), name='moderation-vacancy'),
]
