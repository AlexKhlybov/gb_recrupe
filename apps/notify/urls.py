from django.urls import path

from apps.notify import views as notify


app_name = 'notify'


urlpatterns = [
    path('', notify.MessagesListView.as_view(), name='messages'),
    path('detail/<int:pk>/', notify.MessageDetailView.as_view(), name='detail'),
    path('contact/', notify.contact_view, name='contact'),
    path('success/', notify.success_view, name='success'),
]
