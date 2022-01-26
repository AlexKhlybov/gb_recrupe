import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse

from django.shortcuts import render
from django.views.generic import DetailView, ListView

from apps.main.models import City
from apps.resume.models import Resume, ResumeFavorites, ResumeModeration, Education
from apps.users.models import User


class ResumeListView(ListView):
    model = Resume

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        levels = Education.objects.all()
        context['levels'] = levels
        find = self.request.GET.get('find')
        level = self.request.GET.get('level')
        zero_salary = self.request.GET.get('zerosalary')
        from_salary = self.request.GET.get('fromsalary')
        cityselected = self.request.GET.get('city')
        education = self.request.GET.get('education')
        citysearch = self.request.GET.get('citysearch')
        if cityselected != None and cityselected != '':
            context['cityselected'] = int(cityselected)
        if zero_salary != None:
            context['zero_salary'] = zero_salary
        if from_salary != None and from_salary != '':
            context['from_salary'] = int(from_salary)
        if find != None and find != '':
            context['find'] = find
        if level != None and level != '':
            context['level'] = level
        if education != None and education != '':
            context['education'] = education
        if citysearch != None and citysearch != '':
            context['citysearch'] = citysearch
        context["my_favorites_list_id"] = ResumeFavorites.get_favorite_vacancy_list(self.request.user.id)
        return context

    def get_queryset(self):
        result = [i.id for i in Resume.objects.all()]
        find = self.request.GET.get('find')
        zero_salary = self.request.GET.get('zerosalary')
        city = self.request.GET.get('city')
        from_salary = self.request.GET.get('fromsalary')
        education = self.request.GET.get('education')
        level = self.request.GET.get('level')
        if find != None and find != "":
            find_list = Resume.objects.filter(name__icontains=find)
            result = [i.id for i in find_list]

        # if city != None and city != "":
        #     city_list = [i.id for i in Resume.objects.filter(company__city=city)]
        #     result = list(set(city_list) & set(result))

        if zero_salary != None:
            zero_list = [i.id for i in Resume.objects.filter(price=None)]
            result = list(set(zero_list) & set(result))

        if from_salary != None and from_salary != '':
            from_list = [i.id for i in Resume.objects.filter(price__gte=int(from_salary))]
            result = list(set(from_list) & set(result))

        if education != None and education != '':
            education_list = [i.id for i in Resume.objects.filter(education__educational_institution__icontains=education)]
            result = list(set(education_list) & set(result))

        if level != None and level != '':
            level_list = [i.id for i in Resume.objects.filter(education__level__icontains=level)]
            result = list(set(level_list) & set(result))

        return Resume.objects.filter(pk__in=result)


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
