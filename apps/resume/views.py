import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from apps.resume.forms import ResumeForm, get_resume_data, save_resume_data

from apps.resume.models import Education, Resume, ResumeFavorites, ResumeModeration
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
        context["my_resume"] = Resume.objects.filter(user__pk=self.request.user.pk).order_by("name")
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


@login_required
def create(request):
    return edit(request)


@login_required
def edit(request, pk=None):
    if request.method == 'POST':
        if not request.body:
            # Если пустое тело запроса, то получаем данные
            return JsonResponse(get_resume_data(pk))
        else:
            try:
                body = request.body.decode(encoding='utf-8')
                save_resume_data(request, pk, json.loads(body))
                return JsonResponse({'detail': 'ok'})
            except Exception as e:
                return JsonResponse(status=400, data={'detail': str(e)})

    instance = get_object_or_404(Resume, pk=pk) if pk else None
    if instance and request.user.pk and instance.user.pk != request.user.pk:
        raise PermissionDenied("Доступ к редактированию данного резюме запрещен")
    form = ResumeForm(instance=instance)
    content = {
        'user': instance.user if instance else request.user,
        'form': form,
        'levels': Education.LEVEL_VALUES
    }
    return render(request, 'resume/resume_edit.html', content)


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
