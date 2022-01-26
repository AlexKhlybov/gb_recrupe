# Generated by Django 3.2.11 on 2022-01-18 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('name', models.CharField(db_index=True, max_length=128, verbose_name='Название вакансии')),
                ('description', models.TextField(max_length=5000, verbose_name='Описание вакансии')),
                ('experience', models.PositiveSmallIntegerField(choices=[(1, 'Не имеет значения'), (2, 'от 1 года до 3 лет'), (3, 'от 3 до 6 лет'), (4, 'более 6 лет')], db_index=True, default=1, verbose_name='Опыт работы')),
                ('price_min', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Зарплата от')),
                ('price_max', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Зарплата до')),
                ('is_closed', models.BooleanField(db_index=True, default=False, verbose_name='Признак снятия вакансии')),
                ('is_active', models.BooleanField(db_index=True, default=False, verbose_name='Активен')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancy_company', to='companies.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name_plural': 'Вакансии',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='VacancySkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32, verbose_name='Навык')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancies.vacancy', verbose_name='Вакансия')),
            ],
            options={
                'verbose_name_plural': 'Ключевые навыки вакансии',
            },
        ),
    ]
