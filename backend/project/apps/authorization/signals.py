from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from project.apps.authorization.models import Profile, User, EmailActivateToken


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance: Profile, *args, **kwargs):
    try:
        EmailActivateToken.objects.get(user=instance.user).delete()
    except EmailActivateToken.DoesNotExist:
        pass
    instance.user.delete()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created, **kwargs):
    if instance.is_superuser:
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
