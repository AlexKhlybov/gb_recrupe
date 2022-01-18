from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.users.forms import UserRegisterForm


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

    content = {
    }

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
            return HttpResponseRedirect(reverse('user:login'))
        else:
            messages.add_message(request, messages.ERROR, register_form.errors)
    else:
        register_form = UserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'users/registration.html', content)
