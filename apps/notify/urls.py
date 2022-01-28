from django.urls import path

from apps.notify import views as notify

app_name = 'notify'

urlpatterns = [
    # path('', notify.CompanyListView.as_view(), name='all'),
]
