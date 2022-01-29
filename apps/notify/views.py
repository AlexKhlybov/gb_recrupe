
from urllib import request
from django.shortcuts import render

from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.notify.forms import ContactForm
from apps.notify.models import Notify, NOTIFY_EVENT, TYPE

class MessagesListView(ListView):
    model = Notify
    context_object_name = 'notify'
    
    def get_queryset(self):
        return Notify.objects.filter(user_pk=self.request.user.pk, type=TYPE.MESSAGE).order_by("sent_at")


class MessageDetailView(DetailView):
    pass


def contact_view(request):
    # если метод GET, вернем форму
    if request.method == 'GET':
        form = ContactForm()
    elif request.method == 'POST':
        # если метод POST, проверим форму и отправим письмо
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                Notify.send(
                    user=request.user,
                    event=NOTIFY_EVENT.REGISTRATION_EVENT,
                    type=TYPE.MESSAGE,
                    context={"subject": subject, "message": message},
                    email=from_email,
                )
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('success')
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "notify/email.html", {'form': form})

def success_view(request):
    return HttpResponse('Приняли! Спасибо за вашу заявку.')
