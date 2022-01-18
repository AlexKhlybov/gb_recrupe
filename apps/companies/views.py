from django.views.generic import ListView, DetailView

from apps.companies.models import Company


class CompanyListView(ListView):
    model = Company

    def get_queryset(self):
        return Company.objects.filter(is_active=True)


class CompanyDetailView(DetailView):
    model = Company
