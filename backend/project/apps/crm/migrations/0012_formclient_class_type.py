# Generated by Django 4.1.7 on 2023-03-29 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_formclient_age_formclient_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='formclient',
            name='class_type',
            field=models.CharField(default=1, max_length=100, verbose_name='Тип занятий'),
            preserve_default=False,
        ),
    ]
