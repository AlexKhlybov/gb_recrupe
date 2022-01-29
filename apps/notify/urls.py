from django.urls import path

from apps.notify.views import contact_view, success_view

app_name = 'notify'


urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('success/', success_view, name='success'),
]
