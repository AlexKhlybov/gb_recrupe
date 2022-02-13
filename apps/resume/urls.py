from django.urls import path

from apps.resume import views as resume

app_name = 'resume'

urlpatterns = [
    path('', resume.ResumeListView.as_view(), name='all'),
    path('my/', resume.MyResumeListView.as_view(), name='my'),
    path('<int:pk>/', resume.ResumeDetailView.as_view(), name='detail'),
    path('create/', resume.create, name="create"),
    path('edit/<int:pk>/', resume.edit, name="edit"),

    path('favorites/', resume.FavoritesResumeListView.as_view(), name='favorites'),
    path('edit-favorites/<int:resume>/', resume.favorites_edit, name='favorites-edit'),
    path('complaint/<int:pk>/', resume.complaint, name='complaint'),
]
