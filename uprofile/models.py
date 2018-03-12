from django.db import models
# from django.contrib.auth import get_user_model
# User = get_user_model()

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class UProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    github_uname = models.CharField(max_length=50, null=True, blank=True)
    about = models.TextField(max_length=100, null=True, blank=True)

@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        UProfile.objects.create(user=instance)
