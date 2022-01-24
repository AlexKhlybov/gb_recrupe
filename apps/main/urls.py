from django.urls import path

from apps.main import views as main

app_name = 'main'

urlpatterns = [
    path('', main.HomePageList.as_view(), name='view_list'),
    path('specification/', main.specification, name='specification'),
    path('posting-rules/', main.posting_rules, name='posting_rules'),

]
