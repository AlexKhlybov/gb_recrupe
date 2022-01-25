from re import template

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from apps.resume.models import Resume, ResumeModeration, ResumeFavorites


class ResumeListView(ListView):
    model = Resume
    

class MyResumeListView(ListView):
    model = Resume
    template_name = "resume/my_resume.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Recrupe | Мои резюме"
        context["my_resume"] = Resume.objects.filter(user__pk=self.kwargs["pk"]).order_by("name")
        return context
    

class FavoritesResumeListView(ListView):
    model = ResumeFavorites
    template_name = "resume/favorites_resume.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_favorites"] = ResumeFavorites.get_favorite_resume_from_user(self.request.user.id)
        return context


class ResumeDetailView(DetailView):
    model = Resume
    template_name = "resume/resume_detail.html"


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
