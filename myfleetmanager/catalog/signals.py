from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Owner

@receiver(post_save, sender=User)
def create_owner(sender, instance, created, **kwargs):
    if created:
        # Create an Owner instance for the newly created User
        Owner.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_owner(sender, instance, **kwargs):
    # Save the associated Owner instance when the User is saved
    if hasattr(instance, 'owner'):
        instance.owner.save()