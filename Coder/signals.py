from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Players

@receiver(post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
    if created:
        Players.objects.create(user=instance)