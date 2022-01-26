# Generated by Django 3.2.11 on 2022-01-19 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_alter_companymoderation_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companymoderation',
            name='status',
            field=models.CharField(blank=True, choices=[('Неизвестно', 'Неизвестно'), ('Подтверждено', 'Подтверждено'), ('Запрещено', 'Запрещено')], max_length=100, null=True, verbose_name='Статус'),
        ),
    ]
