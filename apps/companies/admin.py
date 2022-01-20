from import_export import resources
from django.contrib import admin

from apps.companies.models import Company, CompanyModeration

admin.site.register(Company)
admin.site.register(CompanyModeration)

class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
class ModerCompanyResource(resources.ModelResource):
    class Meta:
        model = CompanyModeration