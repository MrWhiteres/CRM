from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from ..authorization.models import User


@receiver(pre_save, sender=User)
def change_type_user(sender, instance: User, *args, **kwargs):
    if instance.user_type == User.USER:
        instance.is_superuser = False
        instance.is_staff = False
        instance.user_group = User.EMPTY
    elif instance.user_type == User.ADMIN:
        instance.is_superuser = True
        instance.is_staff = True
        instance.user_group = User.EMPTY
    elif instance.user_type == User.COACH:
        instance.is_superuser = False
        instance.is_staff = True
        instance.user_group = User.EMPTY
    elif instance.user_type == User.HEAD_COACH:
        instance.is_superuser = False
        instance.is_staff = True
    elif instance.user_type == User.OPERATOR:
        instance.is_superuser = True
        instance.is_staff = True
        instance.user_group = User.EMPTY


@receiver(post_save, sender=User)
def update_model(sender, instance: User, created=False, **kwargs):
    if instance.is_superuser and created:
        instance.is_active = True
        instance.email_verify = True
        instance.user_type = User.ADMIN
        instance.user_group = User.EMPTY
        instance.save(update_fields=['is_active', 'email_verify', 'user_type', 'user_group'])
