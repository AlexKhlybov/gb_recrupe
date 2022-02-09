from webbrowser import get
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import validate_email
from django.contrib.auth.forms import (UserChangeForm, UserCreationForm,
                                       AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserChangeForm, UserCreationForm)
from apps.companies.models import Company

# from .models import ShopUserProfile
from .models import EmployeeProfile, User
from apps.notify.models import Notify, NOTIFY_EVENT, TYPE
from apps.log.logging import logger

from django.contrib.auth.tokens import default_token_generator


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    role = forms.ChoiceField(choices=[x for x in User.USER_TYPE if x[0] != 1], label='Я:', required=True)
    first_name = forms.CharField(label='Фамилия', required=True)
    last_name = forms.CharField(label='Имя', required=True)
    second_name = forms.CharField(label='Отчество', required=False)
    phone = forms.CharField(label='Номер телефона', required=False)
    # specification = forms.BooleanField(label='', required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'role', 'first_name', 'last_name', 'second_name', 'phone',
                  'receiving_messages')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка полей ввода

        for field_name, field in self.fields.items():
            if field_name == 'password1':
                field.label = 'Пароль'
            if field_name == 'password2':
                field.label = 'Подтверждение пароля'

            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            
            if field_name == 'receiving_messages':
                field.widget.attrs['class'] = "form-check-input"
                field.data_err = 'Просто текст'

    # Проверка на уникальность имени пользователя
    def clean_email(self):
        try:
            validate_email(self.cleaned_data['email'])
        except forms.ValidationError as _:
            raise forms.ValidationError('Не корректный email')
        try:
            User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError('Такой почтовый ящик уже зарегистрирован у нас')

    # Проверка совпадения паролей
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('"Пароль" и "Подтверждение пароля" не совпадают')
        return password2

    def save(self, commit=True):
        # user = super(UserRegisterForm, self).save()
        user = super().save()
        user.is_active = False
        user.username = user.email
        if user.role != User.USER_TYPE_MODERATOR:
            # Если не модератор регистрируется, то сразу активируем пользователя
            user.is_active = True
        user.save()

        return user


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'second_name', 'phone', 'password', 'receiving_messages')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка полей ввода

        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.label = 'Пароль'
                field.widget = forms.HiddenInput()

            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            
            if field_name == 'receiving_messages':
                field.widget.attrs['class'] = "form-check-input"


class EmployeeProfileEditForm(UserChangeForm):
    birthday = forms.DateField(input_formats=('%d.%m.%Y', '%Y-%m-%d'))

    class Meta:
        model = EmployeeProfile
        fields = ('skills', 'birthday', 'city', 'gender', 'aboutMe', 'avatar')

    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class CompanyProfileEditForm(UserChangeForm):
    class Meta:
        model = Company
        fields = ('name', 'url', 'city', 'address', 'description', 'logo')

    logo = forms.ImageField(max_length=1024, label='Логотип организации', required=False)

    def __init__(self, *args, **kwargs):
        super(CompanyProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    # def clean_age(self):
    #     data = self.cleaned_data['age']
    #     if data < 18:
    #         raise forms.ValidationError("Вы слишком молоды!")
    #
    #     return data
    #
    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if "yandex" in data:
    #         raise forms.ValidationError("Никто не любит яндекс! =(")
    #     return data


class UserPasswordChangeForm(PasswordChangeForm):
    field_name = ['old_password', 'new_password1', 'new_password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка полей ввода

        for field_name, field in self.fields.items():
            if field_name == 'old_password':
                field.label = 'Старый пароль'
            if field_name == 'new_password1':
                field.label = 'Новый пароль'
            if field_name == 'new_password2':
                field.label = 'Подтверждение пароля'

            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
    
class UserPwdResetForm(PasswordResetForm):
    field_name = ['email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка полей ввода

        for field_name, field in self.fields.items():
            if field_name == 'email':
                field.label = 'E-mail'

            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
    
    def send_mail(self, context):
        """
        Отправка сообщений за счет своего класса Notify
        """
        try:
            # # Отправляем сообщение в личный кабинет! (Для тестов, чтоб Gmail не грузить)
            # Notify.send(user=context['user'], 
            #             event=NOTIFY_EVENT.RESET_PWD_EVENT,
            #             type=TYPE.MESSAGE,
            #             context={"reset_key_link": context['password_reset_key']},)
            # Проверяем готов ли пользователь принимать сообщения
            if context['user'].receiving_messages:
                # Отправляет сообщение на почту
                Notify.send(user=context['user'],
                            event=NOTIFY_EVENT.RESET_PWD_EVENT,
                            type=TYPE.EMAIL,
                            context={"reset_key_link": context['password_reset_key']},)
        except Exception as err:
            logger.error(f"Ошибка отправки сообщения - {err}")
    
    def save(self, domain_override=None, use_https=False, token_generator=default_token_generator,
             request=None, extra_email_context=None, from_email=None, email_template_name=None, subject_template_name=None,
             html_email_template_name=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        try:
            user = User.get_user_by_email(email)
        except Exception as err:
            logger.error(f'Пользователя с таким E-mail не зарегистрирован!')
        user.generate_link(request)
    
        context = {
            'email': email,
            'user': user,
            'password_reset_key': user.password_reset_key,
            **(extra_email_context or {}),
        }
        self.send_mail(context)
        
        
class UserPwdSetForm(SetPasswordForm):
    field_name = ['new_password1', 'new_password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка полей ввода

        for field_name, field in self.fields.items():
            if field_name == 'new_password1':
                field.label = 'Новый пароль'
            if field_name == 'new_password2':
                field.label = 'Подтверждение пароля'

            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
    