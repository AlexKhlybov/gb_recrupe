from django.urls import path

from apps.answers import views as answers

app_name = 'answers'

urlpatterns = [
    path('company_offers/', answers.CompanyOffersListView.as_view(), name='company_offers'),
    path('my_offers/', answers.EmployeeOffersListView.as_view(), name='my_offers'),
    path('company_answers/', answers.CompanyAnswersListView.as_view(), name='company_answers'),
    path('my_answers/', answers.EmployeeAnswersListView.as_view(), name='my_answers'),
    path('vacancy/<int:vacancy_id>/<int:resume_id>/', answers.vacancy_answer, name='vacancy-answer-edit'),
    path('resume/<int:resume_id>/<int:vacancy_id>/', answers.resume_answer, name='resume'),
    path('change/vacancy/<int:pk>/<int:status>/', answers.vacancy_answer_change_status, name='change_vacancy_status'),
     path('change/resume/<int:pk>/<int:status>/', answers.resume_answer_change_status, name='change_resume_status'),
]
