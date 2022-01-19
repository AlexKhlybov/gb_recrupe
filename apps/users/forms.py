# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import UserChangeForm
from django import forms
# from .models import ShopUserProfile
from django.core.validators import validate_email


from .models import User
# import random, hashlib


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    role = forms.ChoiceField(choices=((1, "Работник"), (2, "Работодатель"), (3, "Модератор")), label='Я:',
                             required=True)
    first_name = forms.CharField(label='Фамилия', required=True)
    last_name = forms.CharField(label='Имя', required=True)
    second_name = forms.CharField(label='Отчество', required=False)
    phone = forms.CharField(label='Номер телефона', required=False)
    # specification = forms.BooleanField(label='', required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'role', 'first_name', 'last_name', 'second_name', 'phone', )

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

    # Проверка на уникальность имени пользователя
    def clean_email(self):
        print('email validation')
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
        if user.role != 3:
            # Если не модератор регистрируется, то сразу активируем пользователя
            user.is_active = True
        user.save()

        return user
