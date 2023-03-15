# Generated by Django 4.1.7 on 2023-04-05 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0015_alter_clients_status_coach_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewClientCoach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.clients', verbose_name='Клиент')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Тренер')),
            ],
        ),
    ]