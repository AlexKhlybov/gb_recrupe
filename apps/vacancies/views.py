from tempfile import template

from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from apps.vacancies.models import Vacancy, VacancyModeration, VacancyFavorites


class VacancyListView(ListView):
    model = Vacancy

    def get_queryset(self):
        return Vacancy.objects.all()


class VacancyDetailView(DetailView):
    model = Vacancy


class VacancyCompanyListView(ListView):
    """
    Получить список вакансий компании
    TODO: Объединить с VacancyListView
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
    
    
class FavoritesVacancyListView(ListView):
    model = VacancyFavorites
    template_name = "vacancies/favorites_vacancy.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_favorites"] = VacancyFavorites.get_favorite_vacancy_from_user(self.request.user.id)
        return context
    

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