from django.views.generic import ListView, DetailView

from apps.resume.models import Resume


class ResumeListView(ListView):
    model = Resume


class ResumeDetailView(DetailView):
    model = Resume
