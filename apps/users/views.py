import os
import uuid

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

from apps.companies.models import Company
from apps.users.models import User
from apps.users.forms import (CompanyProfileEditForm, EmployeeProfileEditForm, UserPwdSetForm,
                              UserEditForm, UserRegisterForm, UserPasswordChangeForm, UserPwdResetForm)
from apps.notify.models import Notify, NOTIFY_EVENT, TYPE
from apps.log.logging import logger


def auth_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if not user:
            user_model = get_user_model()
            try:
                find_user = user_model.objects.get(email=username)
                user = auth.authenticate(username=find_user.username if find_user else None, password=password)
            except user_model.DoesNotExist:
                pass
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST:
                url = request.POST.get('next')
                if url:
                    return HttpResponseRedirect(url)
            return HttpResponseRedirect(reverse('main:view_list'))
        else:
            messages.add_message(request, messages.INFO, 'Не верное имя пользователя или пароль')

    content = {}  # TODO - title = 'Вход'

    return render(request, 'users/sign-in.html', content)


def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:view_list'))


def registration(request):
    title = 'Регистрация'
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            try:
                # Отправляем приветственное сообщение после регистрации в ЛК
                Notify.send(event=NOTIFY_EVENT.REGISTRATION_EVENT, type=TYPE.MESSAGE,
                            context={}, email=request.POST["email"],)
            except Exception as err:
                logger.error(f"Пользователь не хочет получать email!")
            if request.POST.get("receiving_messages", False):
                try:
                    # Отправялем EMAIL
                    Notify.send(event=NOTIFY_EVENT.REGISTRATION_EVENT, type=TYPE.EMAIL,
                                context={}, email=request.POST["email"],)
                except Exception as err:
                    logger.error(f"Ошибка отправки сообщения - {err}")
            return HttpResponseRedirect(reverse('user:login'))
        else:
            logger.error(f"Ошибка валидации при регистрации - {register_form.errors}")
            messages.add_message(request, messages.ERROR, register_form.errors)
    else:
        register_form = UserRegisterForm()
    content = {'title': title, 'register_form': register_form}
    return render(request, 'users/registration.html', content)


@login_required
def edit_epmloyee(request):
    title = 'Редактирование профиля сотрудника'
    if request.method == 'POST':
        # print(f'User: {request.user.__dict__}')
        edit_form = UserEditForm(request.POST, instance=request.user)
        profile_form = EmployeeProfileEditForm(request.POST, request.FILES, instance=request.user.employeeprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('user:editemployee'))
        else:
            if not edit_form.is_valid():
                messages.add_message(request, messages.ERROR, edit_form.errors)
            if not profile_form.is_valid():
                messages.add_message(request, messages.ERROR, profile_form.errors)
    else:
        edit_form = UserEditForm(instance=request.user)
        profile_form = EmployeeProfileEditForm(instance=request.user.employeeprofile)

    # print(f'edit_form: {edit_form.__dict__}')

    content = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}
    return render(request, 'users/editemployee.html', content)


@login_required
def edit_company(request):
    title = 'Редактирование профиля компании'
    if request.method == 'POST':
        # print(f'User: {request.user.__dict__}')
        edit_form = UserEditForm(request.POST, instance=request.user)
        profile_form = CompanyProfileEditForm(request.POST, request.FILES, instance=request.user.company)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            if request.user.company:
                # После того как сохранили изменения, отправляем компанию на модерацию
                request.user.company.status = Company.STATUS_MODERATION
                request.user.company.save()
            return HttpResponseRedirect(reverse('user:editcompany'))
        else:
            if not edit_form.is_valid():
                messages.add_message(request, messages.ERROR, edit_form.errors)
            if not profile_form.is_valid():
                messages.add_message(request, messages.ERROR, profile_form.errors)
    else:
        edit_form = UserEditForm(instance=request.user)
        profile_form = CompanyProfileEditForm(instance=request.user.company)

    # print(f'edit_form: {edit_form.__dict__}')

    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
        'company': request.user.company,
    }

    return render(request, 'users/editcompany.html', content)


@login_required
def edit_moderator(request):
    title = 'Редактирование профиля модератора'
    if request.method == 'POST':
        # print(f'User: {request.user.__dict__}')
        edit_form = UserEditForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('user:editmoderator'))
        else:
            if not edit_form.is_valid():
                messages.add_message(request, messages.ERROR, edit_form.errors)
    else:
        edit_form = UserEditForm(instance=request.user)

    content = {
        'title': title,
        'edit_form': edit_form,
    }

    return render(request, 'users/editmoderator.html', content)

# title = 'редактирование'
    #
    # if request.method == 'POST':
    #     edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
    #     profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
    #
    #     if edit_form.is_valid() and profile_form.is_valid():
    #         edit_form.save()
    #         return HttpResponseRedirect(reverse('auth:edit'))
    # else:
    #     edit_form = ShopUserEditForm(instance=request.user)
    #     profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
    #
    # content = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}
    #
    # return render(request, 'authapp/edit.html', content)
    
    
class UserPwdChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "users/pwd_change.html"
    success_url = reverse_lazy("users:pwd_change_done")
    form_class = UserPasswordChangeForm
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            try:
                # Отправляем сообщение в личный кабинет!
                Notify.send(user=user, event=NOTIFY_EVENT.CHANGE_PWD_EVENT,
                                type=TYPE.MESSAGE, context={},)
                # Проверяем готов ли пользователь принимать сообщения
                if user.receiving_messages:
                    # Отправляет сообщение на почту
                    Notify.send(user=user, event=NOTIFY_EVENT.CHANGE_PWD_EVENT,
                                type=TYPE.EMAIL, context={},)
            except Exception as err:
                logger.error(f"Ошибка отправки сообщения - {err}")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    
class UserPwdChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name="users/pwd_change_done.html"
    
    
class UserPwdResetView(PasswordResetView):
    template_name = 'users/pwd_reset.html'
    # email_template_name = "authnapp/password_reset_email.html'
    success_url = reverse_lazy('users:pwd_reset_done')
    form_class = UserPwdResetForm
    
    
class UserPwdResetDoneView(PasswordResetDoneView):
    template_name="users/pwd_reset_done.html"


class UserPwdResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/pwd_reset_confirm.html'
    success_url = reverse_lazy('users:pwd_reset_complete')
    form_class = UserPwdSetForm
    
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        path = self.request.get_full_path()
        host = self.request.get_host()
        reset_link = f'http://{host}{path}'
        self.user = User.objects.filter(password_reset_key=reset_link).first()
        
        if self.request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            if not reset_link:
                return HttpResponse('Нет ссылки для сброса.', status=400)
            if not self.user:
                return HttpResponse('Пользователь не существует', status=400)
            if self.user is not None:
                self.validlink = True
                return self.render_to_response(self.get_context_data())
            # Display the "Password reset unsuccessful" page.
            return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        form.save()
        try:
            # Отправляем сообщение в личный кабинет!
            Notify.send(user=self.user, 
                        event=NOTIFY_EVENT.RESET_PWD_DONE_EVENT,
                        type=TYPE.MESSAGE,
                        context={},)
            # Проверяем готов ли пользователь принимать сообщения
            if self.user.receiving_messages:
                # Отправляет сообщение на почту
                Notify.send(user=self.user,
                            event=NOTIFY_EVENT.RESET_PWD_DONE_EVENT,
                            type=TYPE.EMAIL,
                            context={},)
        except Exception as err:
            logger.error(f"Ошибка отправки сообщения - {err}")
        return HttpResponseRedirect(self.get_success_url())
     

class UserPwdResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/pwd_reset_complete.html'
