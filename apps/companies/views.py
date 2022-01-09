from django.views.generic import ListView, DetailView

from apps.companies.models import Company


class CompanyListView(ListView):
    model = Company

    def get_queryset(self):
        return Company.objects.all()


class CompanyDetailView(DetailView):
    model = Company
