# Generated by Django 4.1.7 on 2023-04-09 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
import project.apps.authorization.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Електронная почта')),
                ('email_verify', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False, verbose_name='Активный')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователь',
            },
        ),
        migrations.CreateModel(
            name='TypeSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', models.CharField(max_length=255, verbose_name='Направление секции')),
            ],
        ),
        migrations.CreateModel(
            name='SectionYoga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_type_section', models.CharField(max_length=255, verbose_name='Тип секции')),
                ('type_section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='authorization.typesection', verbose_name='Направление')),
            ],
        ),
        migrations.CreateModel(
            name='SectionFighter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_type_section', models.CharField(max_length=255, verbose_name='Тип секции')),
                ('type_section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='authorization.typesection', verbose_name='Направление')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_section', models.CharField(blank=True, choices=[('yoga', 'йога'), ('martialArts', 'единоборства')], default=None, max_length=255, null=True, verbose_name='Тип секции')),
                ('type', models.CharField(choices=[('admin', 'Администратор'), ('user', 'Юзер'), ('coach', 'Тренер'), ('head_coach', 'Старший тренер'), ('operator', 'Оператор')], default='user', max_length=20, verbose_name='Тип профиля')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=100, scale=None, size=[1920, 1080], upload_to=project.apps.authorization.models.path_to_image_profile, verbose_name='Изображение профиля')),
                ('phone_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Номер телефона')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профиль пользователя',
            },
        ),
        migrations.CreateModel(
            name='EmailActivateToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_token', models.CharField(blank=True, max_length=255, null=True, verbose_name='Токен')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
