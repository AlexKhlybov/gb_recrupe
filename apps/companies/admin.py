from django.contrib import admin
from import_export import resources

from apps.companies.models import Company

admin.site.register(Company)


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
