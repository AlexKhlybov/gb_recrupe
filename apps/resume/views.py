import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.resume.forms import ResumeForm, get_resume_data, save_resume_data
from apps.main.models import City
from apps.resume.models import Resume, ResumeFavorites, Education
from apps.users.models import User

from apps.resume.models import ResumeSkills


class ResumeListView(LoginRequiredMixin, ListView):
    model = Resume

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        levels = Education.objects.all()
        context['levels'] = levels
        context['resume_skills_list'] = ResumeSkills.objects.all().order_by('name')
        find = self.request.GET.get('find')
        zero_salary = self.request.GET.get('zero_salary')
        from_salary = self.request.GET.get('from_salary')
        to_salary = self.request.GET.get('to_salary')
        resume_skills = self.request.GET.get('resume_skills')
        experience = self.request.GET.get('experience_search')

        if resume_skills is not None:
            context['resume_skills'] = resume_skills
        if zero_salary is not None:
            context['zero_salary'] = zero_salary
        if from_salary is not None and from_salary != '':
            context['from_salary'] = int(from_salary)
        if to_salary is not None and to_salary != '':
            context['to_salary'] = int(to_salary)
        if find is not None:
            context['find'] = find
        if experience is not None and experience != '':
            context['experience_search'] = experience
        context["my_favorites_list_id"] = ResumeFavorites.get_favorite_vacancy_list(self.request.user.id)
        return context

    def get_queryset(self):
        result = [i.id for i in Resume.public.all()]
        find = self.request.GET.get('find')
        zero_salary = self.request.GET.get('zero_salary')
        resume_skills = self.request.GET.get('resume_skills')
        from_salary = self.request.GET.get('from_salary')
        to_salary = self.request.GET.get('to_salary')
        experience = self.request.GET.get('experience_search')
        if find is not None:
            find_list = Resume.objects.filter(name__icontains=find)
            result = [i.id for i in find_list]

        if resume_skills is not None and resume_skills != '':
            resume_skills_list = [i.resume.id for i in ResumeSkills.objects.filter(name=resume_skills)]

            result = list(set(resume_skills_list) & set(result))

        if zero_salary is not None:
            zero_list = [i.id for i in Resume.objects.filter(price=None)]
            result = list(set(zero_list) & set(result))

        if from_salary is not None and from_salary != '':
            from_list = [i.id for i in Resume.objects.filter(price__gte=int(from_salary))]
            result = list(set(from_list) & set(result))

        if to_salary is not None and to_salary != '':
            to_list = [i.id for i in Resume.objects.filter(price__lte=int(to_salary))]
            result = list(set(to_list) & set(result))

        if experience is not None and experience != '':
            experience_list=[]
            id = []

            if experience == "от 1 года до 3 лет":
                id = [1,3]
            if experience == "от 3 до 6 лет":
                id = [3,6]
            if experience == "более 6 лет":
                id = [6,100]

            if len(id)>0:

                for i in Resume.objects.all():
                    if int(id[0]) <= i.get_experience_year <= int(id[1]) :
                        print(i.get_experience_year, i.id)
                        experience_list.append(i.id)

            result = list(set(experience_list) & set(result))
        # if education is not None and education != '':
        #     education_list = [i.id for i in Resume.objects.filter(education__educational_institution__icontains=education)]
        #     result = list(set(education_list) & set(result))
        #
        # if level is not None and level != '':
        #     level_list = [i.id for i in Resume.objects.filter(education__level__icontains=level)]
        #     result = list(set(level_list) & set(result))

        return Resume.public.filter(pk__in=result)


class MyResumeListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = "resume/my_resume.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Recrupe | Мои резюме"
        context["my_resume"] = Resume.objects.filter(user__pk=self.request.user.pk).order_by("name")
        return context
    

class FavoritesResumeListView(LoginRequiredMixin, ListView):
    model = ResumeFavorites
    template_name = "resume/favorites_resume.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites"] = Resume.get_favorite_resume(self.request.user.id)
        return context
    

def favorites_edit(request, resume):
    user = User.objects.get(id=request.user.id)
    resume = Resume.objects.get(id=resume)
    obj, created = ResumeFavorites.objects.get_or_create(user=user, resume=resume)
    if not created:
        obj.delete()
    return JsonResponse({"delete": not created}, status=200)


class ResumeDetailView(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = "resume/resume_detail.html"

    @staticmethod
    def post(request, *args, **kwargs):
        status = request.POST.get('status')
        resume_id = kwargs.get('pk')
        if status and resume_id:
            resume = Resume.objects.filter(pk=resume_id).first()
            resume.status = status
            resume.save()
        return redirect('/moderation/resume/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            context["is_favorite"] = ResumeFavorites.objects.filter(
                user=self.request.user, resume_id=self.kwargs['pk']).exists()
        return context


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


def complaint(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    resume.status = Resume.STATUS_COMPLAINT
    resume.save()
    return JsonResponse({"status": resume.status})
