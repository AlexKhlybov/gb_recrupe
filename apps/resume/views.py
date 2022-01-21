from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from apps.resume.models import Resume, ResumeModeration


class ResumeListView(ListView):
    model = Resume


class ResumeDetailView(DetailView):
    model = Resume


def resume_moderation(request):
    if request.GET.get('find'):
        resume_list = ResumeModeration.objects.filter(
            Q(resume__name__icontains=request.GET.get('find'))
        )
    else:
        resume_list = ResumeModeration.objects.all()
    content = {
        'resume_list': resume_list,
        'title': 'Модерация резюме'
    }
    return render(request, 'moderation/resume_list_moderation.html', content)
