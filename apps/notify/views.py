
from email import message
from urllib import request, response
import json
from django.core.serializers import serialize
from django.utils.safestring import mark_safe
from django.shortcuts import render

from django.core.mail import BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core import serializers
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.notify.forms import ContactForm
from apps.notify.models import Notify, NOTIFY_EVENT, TYPE

class MessagesListView(ListView):
    model = Notify
    context_object_name = 'notify'
    template_name = "notify/messages_list.html"
    
    def get_queryset(self):
        qs = Notify.objects.filter(user__pk=self.request.user.pk, type=TYPE.MESSAGE).order_by("is_read", "-sent_at", )
        return qs


class MessageDetailView(CreateView):
    model = Notify
    context_object_name = 'notify'
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            if not self.request.POST.get("body"):
                # Если пустое тело запроса, то получаем данные
                notify, created = Notify.objects.update_or_create(
                    id=self.kwargs['pk'], 
                    defaults={'is_read': True},
                )
                response = {
                    "title": notify.subject,
                    "text": notify.text,
                    "sender": notify.sender_email,
                    "send_at": notify.send_at.strftime('%Y-%m-%d'),
                    "is_read": notify.is_read
                }
                return JsonResponse(response, status=200)
            else:
                pass
        
    
    # def edit(request, pk=None):
    #     if request.method == 'POST':
    #         if not request.body:
    #             # Если пустое тело запроса, то получаем данные
    #             notify = Notify.objects.get(id=self.kwargs['pk'])
    #             response = {
    #                 "title": notify.subject,
    #                 "text": notify.text,
    #                 "sender": notify.send_email,
    #                 "send_at": notify.send_at,
    #                 "is_read": notify.is_read
    #             }
    #             return JsonResponse(get_resume_data(pk))
    #         else:
    #             try:
    #                 body = request.body.decode(encoding='utf-8')
    #                 save_resume_data(request, pk, json.loads(body))
    #                 return JsonResponse({'detail': 'ok'})
    #             except Exception as e:
    #                 return JsonResponse(status=400, data={'detail': str(e)})

    #     instance = get_object_or_404(Resume, pk=pk) if pk else None
    #     if instance and request.user.pk and instance.user.pk != request.user.pk:
    #         raise PermissionDenied("Доступ к редактированию данного резюме запрещен")
    #     form = ResumeForm(instance=instance)
    #     content = {
    #         'user': instance.user if instance else request.user,
    #         'form': form,
    #         'levels': Education.LEVEL_VALUES
    #     }
    #     return render(request, 'resume/resume_edit.html', content)
        


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
