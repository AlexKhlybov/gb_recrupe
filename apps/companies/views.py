
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from apps.companies.models import Company, CompanyModeration


class CompanyListView(ListView):
    model = Company

    def get_queryset(self):
        return Company.objects.filter(is_active=True)


class CompanyDetailView(DetailView):
    model = Company

def company_moderation(request):

    if request.GET.get('find'):
        company_list= CompanyModeration.objects.filter(
            Q(company__name__icontains=request.GET.get('find'))
        )
    else:
        company_list =CompanyModeration.objects.all()
    content= {
        'company_list':company_list,
        'title': 'Модерация'
    }
    return render(request, 'moderation/company_list_moderation.html', content)

class CompanyModarationUpdateView(UpdateView):
    model = CompanyModeration
    fields = ['status', 'comment']
    template_name = 'moderation/company_moderation.html'
    success_url = reverse_lazy('companies:moderation-companies')



