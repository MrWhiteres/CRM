from django.contrib.admin import register, ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, User


@register(User)
class UserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    model = User


@register(Profile)
class ProfileAdmin(ModelAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'create_at', 'update_at'),
        }),
    )
    list_display = ['user', 'create_at', 'update_at']
    model = Profile
