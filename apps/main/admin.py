from django.contrib import admin
from import_export import resources

from apps.main.models import City

admin.site.register(City)


class CityResource(resources.ModelResource):
    class Meta:
        model = City
