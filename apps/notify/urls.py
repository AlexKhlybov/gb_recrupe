from django.urls import path

from apps.notify import views as notify


app_name = 'notify'


urlpatterns = [
    path('messages', notify.MessagesListView.as_view(), name='massages'),
    path('contact/', notify.contact_view, name='contact'),
    path('success/', notify.success_view, name='success'),
]
