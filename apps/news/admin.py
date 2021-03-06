from django.contrib import admin
from import_export import resources

from apps.news.models import News

admin.site.register(News)


class NewsResource(resources.ModelResource):
    class Meta:
        model = News
