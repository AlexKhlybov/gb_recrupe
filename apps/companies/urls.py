from django.urls import path

from apps.companies import views as companies
from apps.vacancies import views as vacancies

app_name = 'companies'

urlpatterns = [
    path('', companies.CompanyListView.as_view(), name='all'),
    path('<int:pk>/', companies.CompanyDetailView.as_view(), name='detail'),
    path('<int:company_id>/vacancies/', vacancies.VacancyCompanyListView.as_view(), name='vacancies'),
]
