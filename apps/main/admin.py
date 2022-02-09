from django.contrib import admin
from import_export import resources
from solo.admin import SingletonModelAdmin

from apps.main.models import City
from apps.main.models import SiteConfiguration


admin.site.register(City)
admin.site.register(SiteConfiguration, SingletonModelAdmin)

class CityResource(resources.ModelResource):
    class Meta:
        model = City


class SiteConfigurationResource(resources.ModelResource):
    class Meta:
        model = SiteConfiguration