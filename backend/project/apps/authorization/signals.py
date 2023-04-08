from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from ..authorization.models import Profile, User, EmailActivateToken


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance: Profile, *args, **kwargs):
    try:
        EmailActivateToken.objects.get(user=instance.user).delete()
    except EmailActivateToken.DoesNotExist:
        pass
    instance.user.delete()


@receiver(pre_save, sender=Profile)
def change_type_user(sender, instance: Profile, *args, **kwargs):
    match instance.type:
        case Profile.USER:
            instance.user.is_superuser = False
            instance.user.is_staff = False
        case Profile.ADMIN:
            instance.user.is_superuser = True
            instance.user.is_staff = True
        case Profile.COACH:
            instance.user.is_superuser = False
            instance.user.is_staff = True
        case Profile.HEAD_COACH:
            instance.user.is_superuser = False
            instance.user.is_staff = True
        case Profile.OPERATOR:
            instance.user.is_superuser = True
            instance.user.is_staff = True
    instance.user.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created, **kwargs):
    if instance.is_superuser:
        if created:
            Profile.objects.create(user=instance, type=Profile.ADMIN)
            instance.is_active = True
            instance.email_verify = True
            instance.profile.save()
