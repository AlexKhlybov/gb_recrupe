import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from apps.resume.forms import ResumeForm, get_resume_data, save_resume_data
from apps.resume.models import Resume, ResumeModeration, Education


class ResumeListView(ListView):
    model = Resume


class ResumeDetailView(DetailView):
    model = Resume


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
                print(e)
                raise e
                return JsonResponse(status=400, data={'detail': str(e)})

    instance = get_object_or_404(Resume, pk=pk) if pk else None
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
