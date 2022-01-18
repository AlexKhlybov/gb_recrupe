from django.views.generic import ListView, DetailView

from apps.vacancies.models import Vacancy


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
