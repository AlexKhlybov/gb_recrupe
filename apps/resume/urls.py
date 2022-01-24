from django.urls import path

from apps.resume import views as resume

app_name = 'resume'

urlpatterns = [
    path('', resume.ResumeListView.as_view(), name='all'),
    path('my-resume/<int:pk>/', resume.MyResumeListView.as_view(), name='my-resume'),
    path('<int:pk>/', resume.ResumeDetailView.as_view(), name='detail'),
    path('moderation-resume/', resume.resume_moderation, name='moderation-resume'),

]
