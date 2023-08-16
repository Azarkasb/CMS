from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from financial.models import Wallet


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    print('something craette')
    if created:
        Wallet.objects.create(user=instance)