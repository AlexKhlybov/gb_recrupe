from django.urls import path

from apps.vacancies import views as vacancies

app_name = 'vacancies'

urlpatterns = [
    path('', vacancies.VacancyListView.as_view(), name='all'),
    path('<int:pk>/', vacancies.VacancyDetailView.as_view(), name='detail'),
    path('create/', vacancies.create, name="create"),
    path('edit/<int:pk>/', vacancies.edit, name="edit"),
    path('my/', vacancies.MyVacancyCompanyListView.as_view(), name='my'),

    path('favorites/<pk>/', vacancies.FavoritesVacancyListView.as_view(), name='favorites'),
    path('edit-favorites/<vacancy>/', vacancies.favorites_edit, name='favorites-edit'),
    path('complaint/<int:pk>/', vacancies.complaint, name='complaint'),
]
