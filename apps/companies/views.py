from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.companies.models import Company
from apps.users.models import User


class CompanyListView(ListView):
    model = Company

    def get_queryset(self):
        where = Q(status=Company.STATUS_PUBLIC)
        user = self.request.user
        if user and user.pk:
            where = where | Q(user=user)
        if user and user.pk and user.role == User.USER_TYPE_MODERATOR:
            return Company.public.select_related()
        return Company.public.select_related().filter(where)


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company

    @staticmethod
    def post(request, *args, **kwargs):
        company_id = kwargs.get('pk')
        status = request.POST.get('status')
        if request.user.role == User.USER_TYPE_MODERATOR and status and company_id:
            company = Company.objects.filter(pk=company_id).first()
            company.status = status
            company.save()
        return redirect('/moderation/companies/')
