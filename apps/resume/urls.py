from django.urls import re_path, path

from apps.resume import views as resume

app_name = 'resume'

urlpatterns = [
    re_path(r'^$', resume.ResumeListView.as_view(), name='all'),
    # re_path(r'^my-resume/(?P<pk>\d+)/$', resume.MyResumeListView.as_view(), name='my-resume'),
    path('my/', resume.MyResumeListView.as_view(), name='my'),
    re_path(r'^(?P<pk>\d+)/$', resume.ResumeDetailView.as_view(), name='detail'),
    
    re_path(r'^favorites/(?P<pk>\d+)/$', resume.FavoritesResumeListView.as_view(), name='favorites'),
    re_path(r'^edit-favorites/(?P<resume>\d+)/$', resume.favorites_edit, name='favorites-edit'),
    
    re_path(r'^moderation-resume/$', resume.resume_moderation, name='moderation-resume'),
    
    re_path(r'^create/$', resume.create, name="create"),
    re_path(r'^edit/(?P<pk>\d+)/$', resume.edit, name="edit"),
]
