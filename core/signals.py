from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Profile when a new User is saved.
    Also update an existing profile when a User is updated.
    This prevents RelatedObjectDoesNotExist errors throughout the app.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # Ensure profile always exists even for older accounts
        Profile.objects.get_or_create(user=instance)
