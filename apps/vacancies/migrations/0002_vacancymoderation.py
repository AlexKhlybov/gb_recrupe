# Generated by Django 3.2.11 on 2022-01-19 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VacancyModeration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('Неизвестно', 'Неизвестно'), ('Подтверждено', 'Подтверждено'), ('Запрещено', 'Запрещено')], max_length=100, null=True, verbose_name='Статус')),
                ('comment', models.TextField(blank=True, verbose_name='Комментрарий модератора')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Время отпраления комментария')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancies.vacancy')),
            ],
            options={
                'verbose_name': 'Модерация вакансии ',
                'verbose_name_plural': 'Модерация вакансии',
            },
        ),
    ]