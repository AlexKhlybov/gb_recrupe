from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import CreateView, ListView

from apps.notify.forms import ContactForm
from apps.notify.models import NOTIFY_EVENT, TYPE, Notify
from apps.users.models import User

from log.logging import logger

class MessagesListView(LoginRequiredMixin, ListView):
    model = Notify
    context_object_name = "notify"
    template_name = "notify/messages_list.html"

    def get_queryset(self):
        qs = Notify.objects.filter(user__pk=self.request.user.pk, type=TYPE.MESSAGE).order_by("is_read", "-sent_at",)
        return qs


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Notify
    context_object_name = "notify"

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            if request.POST.get("id"):
                notify, created = Notify.objects.update_or_create(
                    id=request.POST.get("id"), defaults={"is_read": True},
                )
                response = {
                    "title": notify.subject,
                    "text": notify.text,
                    "sender": notify.sender_email,
                    "send_at": notify.send_at.strftime("%Y-%m-%d"),
                    "is_read": notify.is_read,
                }
                return JsonResponse(response, status=200)
            else:
                body = request.POST
                recipient = User.get_user_by_email(body["email"])
                Notify.objects.create(
                    subject=body["subject"],
                    text=body["text"],
                    user=recipient,
                    email=body["email"],
                    sender_email=request.user.email,
                    type=TYPE.MESSAGE,
                    event=NOTIFY_EVENT.MESSAGE,
                    send_at=timezone.now(),
                    sent_at=timezone.now(),
                )
                if recipient.receiving_messages:
                    # Отправляем уведомление на почту о получении сообщении.
                    try:
                        Notify.send(event=NOTIFY_EVENT.MESSAGE,
                                    type=TYPE.EMAIL,
                                    context={},
                                    email=body["email"],)
                    except Exception as err:
                        logger.error(f"Ошибка отправки сообщения - {err}")
                return JsonResponse({"detail": "Ok"}, status=200)


def contact_view(request):
    # если метод GET, вернем форму
    if request.method == "GET":
        form = ContactForm()
    elif request.method == "POST":
        # если метод POST, проверим форму и отправим письмо
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            message = form.cleaned_data["message"]
            try:
                Notify.send(
                    user=request.user,
                    event=NOTIFY_EVENT.REGISTRATION_EVENT,
                    type=TYPE.MESSAGE,
                    context={"subject": subject, "message": message},
                    email=from_email,
                )
            except BadHeaderError:
                return HttpResponse("Ошибка в теме письма.")
            return redirect("success")
    else:
        return HttpResponse("Неверный запрос.")
    return render(request, "notify/email.html", {"form": form})


def success_view(request):
    return HttpResponse("Приняли! Спасибо за вашу заявку.")
