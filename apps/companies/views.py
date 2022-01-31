from django.db.models import Q
from django.views.generic import DetailView, ListView, LoginRequiredMixin

from apps.companies.models import Company
from apps.users.models import User


class CompanyListView(LoginRequiredMixin, ListView):
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
