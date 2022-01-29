from django.db import models
from django.conf import settings
from django.template import Template, Context

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL
from django.utils.timezone import now

from apps.log.logging import logger

# logger = logging.getLogger(__name__)


#     Notify.send(
#         user=user,
#         event=settings.NOTIFY_EVENT_RESTORE_PASSWORD,
#         context={'password_reset_key': user.password_reset_key},
#         email=email,
#     )

class SMTPAccount(models.Model):
    host = models.CharField(default='smtp.yandex.ru', max_length=255, verbose_name='Хост')
    port = models.IntegerField(default=587, verbose_name='Порт')
    is_use_tls = models.BooleanField(default=True, verbose_name='Использовать TLS?')
    is_use_ssl = models.BooleanField(default=False, verbose_name='Использовать SSL?')
    sender = models.EmailField(max_length=255, blank=True, default='', verbose_name='Отправитель')
    username = models.CharField(max_length=255, blank=True, default='', verbose_name='Имя пользователя')
    password = models.CharField(max_length=255, blank=True, default='', verbose_name='Пароль пользователя')

    is_active = models.BooleanField(default=True, verbose_name='Включить аккаунт')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    @classmethod
    def get_free_smtp(cls):
        """
        Проверяет и отдает один аккаунт SMTP, с которого можно отправить письмо
        """   
        accounts = cls.objects.filter(is_active=True).distinct()

        for account in accounts:
            logger.warning(f"Выбран клиент отправки сообщений - {account.host}")
            return account

    def __str__(self):
        return '{} ({}:{})'.format(self.username, self.host, self.port)


    class Meta:
        verbose_name = 'SMTP аккаунт'
        verbose_name_plural = 'SMTP аккаунты'


class TYPE:
    EMAIL = 0
    MESSAGE = 1

    CHOICES = (
        (EMAIL, 'E-mail'),
        (MESSAGE, 'Message'),
    )


class NOTIFY_EVENT:
    # notify events
    REGISTRATION_EVENT = 1
    FEEDBACK_EVENT = 2
    MESSAGE= 3

    CHOICES_NOTIFY_EVENT = {
        REGISTRATION_EVENT: {
            'title': 'Register',
        },
        FEEDBACK_EVENT: {
            'title': 'Feeback',
        },
        MESSAGE: {
            'title': 'Message',
        },
    }

    CHOICES = [(k, v['title']) for k, v in CHOICES_NOTIFY_EVENT.items()]


class NotifyTemplate(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название для админа')
    subject = models.CharField(max_length=255, default='', blank=True, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Пользователь (получатель)')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Email получатель', help_text='Используется только в случае отсутствия указанного пользователя')

    type = models.IntegerField(choices=TYPE.CHOICES, verbose_name='Тип')
    event = models.IntegerField(choices=NOTIFY_EVENT.CHOICES, blank=True, null=True, verbose_name='Событие')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    send_at = models.DateTimeField(blank=True, null=True, verbose_name='Время начала отправки')

    def render_subject(self, ct):
        template = Template(self.subject)
        context = Context(ct)
        return template.render(context)

    def render_text(self, ct):
        template = Template(self.text)
        context = Context(ct)
        return template.render(context)

    def get_event_data(self):
        return settings.NOTIFY_EVENTS[self.event]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'


class Notify(models.Model):
    """
    Уведомление
    """
    # title = models.CharField(max_length=255, verbose_name='Название для админа')
    subject = models.CharField(max_length=255, default='', blank=True, verbose_name='Тема')
    text = models.TextField(verbose_name='Текст')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='notifies', verbose_name='Пользователь (получатель)')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Email Получателя',
                              help_text='Используется только в случае отсутствия указанного пользователя')
    sender_email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Email Отправителя')
    
    type = models.IntegerField(choices=TYPE.CHOICES, verbose_name='Тип')
    event = models.IntegerField(choices=NOTIFY_EVENT.CHOICES, blank=True, null=True, verbose_name='Событие')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    send_at = models.DateTimeField(blank=True, null=True, verbose_name='Время начала отправки')
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата отправки')

    def __str__(self):
        return self.subject

    def get_sender(self):
        pass

    def _send(self):
        # if self.user:
            # self.email = self.user.email

        if self.type == TYPE.EMAIL:
            self.send_email()
        if self.type == TYPE.MESSAGE:
            self.send_message()

        self.save()

    def send_email(self):
        account = SMTPAccount.get_free_smtp()
        self.sender_email = account.sender

        try:
            body = self._render_body(account.sender)
            server = SMTP_SSL(account.host, account.port) if account.is_use_ssl else SMTP(account.host, account.port)
            server.ehlo()
            if account.is_use_tls:
                server.starttls()
            server.login(account.username, account.password)
            server.sendmail(account.sender, [self.email], body.as_string())
            server.close()
            self.sent_at = now()
            
            logger.info(f"Email успешно отправлен на адрес - {account.sender}")
        except Exception as err:  # noqa
            logger.error(err)

    def send_message(self):

        if self.user is None:
            print("WARNING!!! Нет такого пользователя!")
            self.save()
            return

        self.sent_at = now()
        self.save()

    @staticmethod
    def send(event, context, user=None, email=None):

        if user:
            email = user.email if not email else email

        # Для выбора шаблонов в action'е
        template = NotifyTemplate.objects.get(event=event, is_active=True)

        # Формируем список основных и дополнительных получателей письма
        # Первого получателя заполняем из шаблона, его данные могут быть пустыми - чтобы можно было через
        # код отправить уведомление
        if template.user or template.email:
            reciever = {
                'user': template.user,
                'email': template.email,
            }
        elif user or email:
            reciever = {
                'user': user,
                'email': email,
            }
        else:
            logger.info(f"Нет получателя!")
            recievers = ''

        template_user = reciever['user']
        template_email = reciever['email']
        # Если в шаблоне не указан получатель, то получатель тот, кого передали в коде
        if template_user is None and template_email is None:
            template_user = user
            template_email = email
            # Если пользователь заполнен, то перезаписываем поля емейла
            # даже если они были переданы.
            if user is not None:
                template_email = user.email
        local_context = context.copy()

        # Добавляем пользователя в контекст, если его там не передали
        if template_user is not None:
            if local_context is not None:
                local_context.update({
                    'user': template_user,
                })
            else:
                local_context = {
                    'user': template_user,
                }
        local_context['event_id'] = event

        instance = Notify.objects.create(
            subject=template.render_subject(local_context),
            text=template.render_text(local_context),
            user=template_user,
            email=template_email,
            type=template.type,
            event=template.event,
            send_at=template.send_at,
        )
        instance._send()
        return

    def _render_body(self, mail_from):
        msg = MIMEMultipart('alternative')

        msg['Subject'] = self.subject
        msg['From'] = mail_from
        msg['To'] = self.email

        text = MIMEText(self.text, 'plain')
        msg.attach(text)

        return msg

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
