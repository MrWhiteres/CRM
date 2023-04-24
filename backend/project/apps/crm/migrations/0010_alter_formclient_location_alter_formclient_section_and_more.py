# Generated by Django 4.2 on 2023-04-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_alter_coachforclient_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formclient',
            name='location',
            field=models.ManyToManyField(blank=True, to='crm.location', verbose_name='Локации которые были выбраны(ID)'),
        ),
        migrations.AlterField(
            model_name='formclient',
            name='section',
            field=models.ManyToManyField(blank=True, to='crm.section', verbose_name='Секции которое были выбраны(ID)'),
        ),
        migrations.AlterField(
            model_name='formclient',
            name='visit_time',
            field=models.ManyToManyField(blank=True, to='crm.alltime', verbose_name='Время которое было выбрано(ID)'),
        ),
        migrations.AlterField(
            model_name='otherdata',
            name='location',
            field=models.ManyToManyField(blank=True, to='crm.location', verbose_name='Локации которые были выбраны(TEXT)'),
        ),
        migrations.AlterField(
            model_name='otherdata',
            name='section',
            field=models.ManyToManyField(blank=True, to='crm.section', verbose_name='Секции которое были выбраны(TEXT)'),
        ),
    ]