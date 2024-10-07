from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Owner

@receiver(post_save, sender=User)
def create_or_update_owner(sender, instance, created, **kwargs):
    if created:
        Owner.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)
    else:
        if hasattr(instance, 'owner'):
            instance.owner.first_name = instance.first_name
            instance.owner.last_name = instance.last_name
            instance.owner.save()