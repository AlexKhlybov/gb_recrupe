from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.users.forms import UserRegisterForm, UserEditForm, EmployeeProfileEditForm, CompanyProfileEditForm


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

    content = {}

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

def edit_company(request):
    title = 'Редактирование профиля компании'
    if request.method == 'POST':
        # print(f'User: {request.user.__dict__}')
        edit_form = UserEditForm(request.POST, instance=request.user)
        profile_form = CompanyProfileEditForm(request.POST, request.FILES, instance=request.user.company)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
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

    content = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}

    return render(request, 'users/editcompany.html', content)



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
