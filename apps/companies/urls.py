from django.urls import path

from apps.companies import views as companies

app_name = 'companies'

urlpatterns = [
    path('', companies.CompanyListView.as_view(), name='all'),
    path('<int:pk>/', companies.CompanyDetailView.as_view(), name='detail'),
]
