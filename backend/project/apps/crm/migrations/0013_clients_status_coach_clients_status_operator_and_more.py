# Generated by Django 4.1.7 on 2023-04-01 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_formclient_class_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='status_coach',
            field=models.CharField(choices=[('not_check', 'Не проверен'), ('checked_upload', 'Проверен, записан'), ('checked_closed', 'Проверен, отказ')], default='not_check', max_length=255, verbose_name='Cтатус проверки тренера'),
        ),
        migrations.AddField(
            model_name='clients',
            name='status_operator',
            field=models.CharField(choices=[('not_check', 'Не проверен'), ('checked_upload', 'Проверен, записан'), ('checked_closed', 'Проверен, отказ')], default='not_check', max_length=255, verbose_name='Статус оператора'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='status',
            field=models.CharField(choices=[('new', 'Новый клиент'), ('refusal', 'Отказ'), ('recorded', 'Записан'), ('on_check', 'На проверке')], default='new', max_length=255, verbose_name='Статус клиента'),
        ),
        migrations.DeleteModel(
            name='UserSection',
        ),
    ]
