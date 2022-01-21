from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from apps.companies.models import Company, CompanyModeration
from apps.users.models import User


class CompanyListView(ListView):
    model = Company

    def get_queryset(self):
        where = Q(is_active=True)
        user = self.request.user
        if user and user.pk:
            where = where | Q(user=user)

        if user and user.pk and user.role == User.USER_TYPE_MODERATOR:
            return Company.objects.select_related()
        return Company.objects.select_related().filter(where)


class CompanyDetailView(DetailView):
    model = Company


def company_moderation(request):
    if request.GET.get('find'):
        company_list = CompanyModeration.objects.filter(
            Q(company__name__icontains=request.GET.get('find'))
        )
    else:
        company_list = CompanyModeration.objects.all()

    content = {
        'company_list': company_list,
        'title': 'Модерация'
    }
    return render(request, 'moderation/company_list_moderation.html', content)


class CompanyModarationUpdateView(UpdateView):
    model = CompanyModeration
    fields = ['status', 'comment']
    template_name = 'moderation/company_moderation.html'
    success_url = reverse_lazy('companies:moderation-companies')
