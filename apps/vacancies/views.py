from tempfile import template

from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from apps.main.models import City
from apps.vacancies.models import Vacancy, VacancyModeration


class VacancyListView(ListView):
    model = Vacancy


class VacancyListView(ListView):
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cities = City.objects.all().order_by('city')
        context['cities'] = cities
        find = self.request.GET.get('find')
        zero_salary = self.request.GET.get('zerosalary')
        from_salary = self.request.GET.get('fromsalary')
        cityselected = self.request.GET.get('city')
        company_id = self.request.GET.get('company_id')
        citysearch = self.request.GET.get('citysearch')
        if cityselected != None and cityselected != '':
            context['cityselected'] = int(cityselected)
        if zero_salary != None:
            context['zero_salary'] = zero_salary
        if from_salary != None and from_salary != '':
            context['from_salary'] = int(from_salary)
        if find != None and find != '':
            context['find'] = find
        if company_id != None and company_id != '':
            context['company_id'] = company_id
        if citysearch != None and citysearch != '':
            context['citysearch'] = citysearch
        return context

    def get_queryset(self):
        result = [i.id for i in Vacancy.objects.all()]
        find = self.request.GET.get('find')
        zero_salary = self.request.GET.get('zerosalary')
        city = self.request.GET.get('city')
        from_salary = self.request.GET.get('fromsalary')
        company_id = self.request.GET.get('company_id')
        if find != None and find != "":
            find_list = Vacancy.objects.filter(name__icontains=find)
            result = [i.id for i in find_list]

        if city != None and city != "":
            city_list = [i.id for i in Vacancy.objects.filter(company__city=city)]
            result = list(set(city_list) & set(result))

        if zero_salary != None:
            zero_list = [i.id for i in Vacancy.objects.filter(price_min=None, price_max=None)]
            result = list(set(zero_list) & set(result))

        if from_salary != None and from_salary != '':
            from_list = [i.id for i in Vacancy.objects.filter(price_min__gte=int(from_salary))]
            result = list(set(from_list) & set(result))

        if company_id != None and company_id != '':
            company_list = [i.id for i in Vacancy.objects.filter(company__name__icontains=company_id)]
            result = list(set(company_list) & set(result))

        return Vacancy.objects.filter(pk__in=result)


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
