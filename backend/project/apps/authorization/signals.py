from django.db.models.signals import pre_save
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
