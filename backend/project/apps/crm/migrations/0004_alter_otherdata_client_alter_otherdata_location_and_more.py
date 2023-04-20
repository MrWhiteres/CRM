# Generated by Django 4.2 on 2023-04-19 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_alter_formclient_age_alter_formclient_class_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherdata',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.clients'),
        ),
        migrations.AlterField(
            model_name='otherdata',
            name='location',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Локации которые были выбраны(TEXT)'),
        ),
        migrations.AlterField(
            model_name='otherdata',
            name='section',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Секции которое были выбраны(TEXT)'),
        ),
    ]