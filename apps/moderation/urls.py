from django.urls import path

from apps.moderation import views as moderation

app_name = 'moderation'

urlpatterns = [
    path('companies/', moderation.company_moderation, name='companies'),
    path('<int:pk>/moderation-company/', moderation.CompanyModerationUpdateView.as_view(), name='moderation-company'),
    path('resume/', moderation.resume_moderation, name='resume'),
    path('vacancy/', moderation.vacancy_moderation, name='vacancy'),
]
