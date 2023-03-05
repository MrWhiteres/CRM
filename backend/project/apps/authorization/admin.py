from django.contrib.admin import register, ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, User


@register(User)
class UserAdmin(UserAdmin):
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name')}),
        ('Параметры доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # ('Параметры доступа', {'fields': ('is_active', 'is_staff', 'is_superuser',
        #                                   'groups', 'user_permissions')}),
        ('Посещаемость', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    model = User


@register(Profile)
class ProfileAdmin(ModelAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('image', 'phone_number', 'type', 'create_at', 'update_at'),
        }),
    )
    list_display = ['user', 'type', 'create_at', 'update_at']
    model = Profile
