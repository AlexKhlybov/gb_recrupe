import os
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def upload_to_employee_profile(instance, filename):
    if instance.pk:
        try:
            profile = EmployeeProfile.objects.filter(pk=instance.pk).first()
            if profile and profile.avatar:
                profile.avatar.delete()
        except (OSError, FileNotFoundError) as _:
            pass
    ext = filename.split('.')[-1]
    return os.path.join('users', f'{uuid4()}.{ext}')


class User(AbstractUser):
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    USER_TYPE_MODERATOR = 1  # Модератор
    USER_TYPE_EMPLOYEE = 2   # Соискатель
    USER_TYPE_EMPLOYER = 3   # Работодатель

    USER_TYPE = (
        (USER_TYPE_EMPLOYEE, 'Соискатель'),
        (USER_TYPE_EMPLOYER, 'Работодатель'),
        (USER_TYPE_MODERATOR, 'Модератор'),
    )

    username = models.EmailField(unique=True, db_index=True, verbose_name='Почта')
    first_name = models.CharField(max_length=32, verbose_name='Имя')
    last_name = models.CharField(max_length=32, verbose_name='Фамилия')
    second_name = models.CharField(max_length=32, blank=True, verbose_name='Отчество')
    phone = models.CharField(max_length=16, blank=True, verbose_name='Номер телефона')
    role = models.PositiveSmallIntegerField(choices=USER_TYPE, default=USER_TYPE_MODERATOR, verbose_name='Роль')
    receiving_messages = models.BooleanField(default=False, verbose_name='Получать уведомления на e-mail')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_role_name(self):
        for item in self.USER_TYPE:
            if item[0] == self.role:
                return item[1]
        return None

    def __str__(self):
        return f'{self.username}'
    
    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name} {self.second_name}'
    
    @staticmethod
    def get_user_by_email(email):
        return User.objects.get(email=email)

      
class EmployeeProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    skills = models.CharField(max_length=500, verbose_name='навыки', blank=True)
    birthday = models.DateField(null=True, blank=True, verbose_name='дата рождения')
    city = models.CharField(max_length=100, verbose_name='город', blank=True)
    aboutMe = models.TextField(max_length=5000, verbose_name='о себе',  blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='пол')
    avatar = models.FileField(max_length=64, null=True, verbose_name='Фотография', blank=True,
                              upload_to=upload_to_employee_profile)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            if instance.role == User.USER_TYPE_EMPLOYEE:
                EmployeeProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.role == User.USER_TYPE_EMPLOYEE:
            instance.employeeprofile.save()
