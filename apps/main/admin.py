from import_export import resources
from django.contrib import admin

from apps.main.models import City

admin.site.register(City)


class CityResource(resources.ModelResource):
    class Meta:
        model = City
