from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name_plural = 'User - Пользователи'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    USER_TYPE_MODERATOR = 1
    USER_TYPE_EMPLOYEE = 2
    USER_TYPE_EMPLOYER = 3

    USER_TYPE = (
        (USER_TYPE_EMPLOYEE, 'Сотрудник'),
        (USER_TYPE_EMPLOYER, 'Работодатель'),
        (USER_TYPE_MODERATOR, 'Модератор'),
    )

    username = models.EmailField(unique=True, db_index=True, verbose_name='Почта')
    first_name = models.CharField(max_length=32, verbose_name='Имя')
    last_name = models.CharField(max_length=32, verbose_name='Фамилия')
    second_name = models.CharField(max_length=32, blank=True, verbose_name='Отчество')
    phone = models.CharField(max_length=16, blank=True, verbose_name='Номер телефона')
    role = models.PositiveSmallIntegerField(choices=USER_TYPE, default=USER_TYPE_MODERATOR, verbose_name='Роль')

    def get_role_name(self):
        for item in self.USER_TYPE:
            if item[0] == self.role:
                return item[1]
        return None

    def __str__(self):
        return f'{self.username}'
