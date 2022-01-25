from re import template

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from apps.resume.models import Resume, ResumeFavorites, ResumeModeration
from apps.users.models import User


class ResumeListView(ListView):
    model = Resume
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_favorites_list_id"] = ResumeFavorites.get_favorite_vacancy_list(self.request.user.id)
        return context
    

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
        context["favorites"] = Resume.get_favorite_resume(self.request.user.id)
        return context
    
    
def favorites_edit(request, resume):
    user = User.objects.get(id=request.user.id)
    resume = Resume.objects.get(id=resume)
    obj, created = ResumeFavorites.objects.get_or_create(
        user=user,
        resume=resume,)
    if not created:
        obj.delete()
        return JsonResponse({"delete": True}, status=200)
    return JsonResponse({"delete": False}, status=200)


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
