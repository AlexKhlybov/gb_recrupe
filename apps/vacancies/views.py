from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from apps.users.models import User
from apps.vacancies.forms import VacancyForm
from apps.vacancies.models import Vacancy, VacancyModeration


class VacancyListView(ListView):
    model = Vacancy

    def get_queryset(self):
        return Vacancy.objects.all()


class VacancyDetailView(DetailView):
    model = Vacancy


class VacancyCompanyListView(ListView):
    """
    Получить список вакансий компании
    Объединить с VacancyListView
    """
    model = Vacancy

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        return Vacancy.objects.filter(company_id=company_id, is_closed=False, is_active=True)
    
    
class MyVacancyCompanyListView(VacancyCompanyListView):
    template_name = "vacancies/my_vacancy.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["template"] = "Recrupe | Мои вакансии"
        return context
    

@login_required
def create(request):
    return edit(request)


@login_required
def edit(request, pk=None):
    vacancy = Vacancy.objects.filter(pk=pk).first()
    user = User.objects.filter(pk=request.user.pk).first()
    if pk and user.pk != vacancy.company.user.pk and user.role != User.USER_TYPE_MODERATOR:
        raise PermissionDenied("Доступ к данной вакансии запрещен")

    if request.method == 'POST':
        instance = get_object_or_404(Vacancy, pk=pk) if pk else None
        form = VacancyForm(request.POST, instance=instance)
        if form.is_valid():
            try:
                form.save(company=request.user.company)
                return redirect(f'/companies/{request.user.company.pk}/my-vacancies/')
            except Exception as e:
                raise e
                # form.add_error(None, str(e))
        else:
            print(form.errors)

    skills = [x.name for x in vacancy.skills] if vacancy else []
    instance = get_object_or_404(Vacancy, pk=pk) if pk else None
    form = VacancyForm(instance=instance, initial={'skills': ','.join(skills)})
    content = {
        'form': form,
    }
    return render(request, 'vacancies/vacancy_edit.html', content)


def vacancy_moderation(request):
    if request.GET.get('find'):
        vacancy_list = VacancyModeration.objects.filter(
            Q(vacancy__name__icontains=request.GET.get('find'))
        )
    else:
        vacancy_list = VacancyModeration.objects.all()
    content = {
        'vacancy_list': vacancy_list,
        'title': 'Модерация вакансии'
    }
    return render(request, 'moderation/vacancy_list_moderation.html', content)


class VacancyModarationUpdateView(UpdateView):
    model = VacancyModeration
    fields = ['status', 'comment']
    template_name = 'moderation/vacancy_moderation.html'
    success_url = reverse_lazy('vacancies:moderation-vacancy')
