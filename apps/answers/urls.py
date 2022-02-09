from django.urls import path

from apps.answers import views as answers

app_name = 'answers'

urlpatterns = [
    path('company_offers/<pk>/', answers.CompanyOffersListView.as_view(), name='company_offers'),
    path('my_offers/<pk>/', answers.EmployeeOffersListView.as_view(), name='my_offers'),
    path('company_answers/<pk>/', answers.CompanyAnswersListView.as_view(), name='company_answers'),
    path('my_answers/<pk>/', answers.EmployeeAnswersListView.as_view(), name='my_answers'),
    path('edit-vacancy-answer/<int:vacancy>/<str:resume_name>/', answers.vacancy_answer_edit, name='vacancy-answer-edit'),
    path('edit-resume-answer/<int:resume>/<str:vacancy_name>/', answers.resume_answer_edit, name='resume-answer-edit'),
]
