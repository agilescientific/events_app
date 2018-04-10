from django.db import models
# from django.contrib.auth import get_user_model
# User = get_user_model()

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class UProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    github_uname = models.CharField(max_length=50, null=True, blank=True)
    about = models.TextField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to=user_directory_path,  null=True, blank=True,
                                    default='default/blank-profile.png')

    class Meta:
        verbose_name = 'Extender User Profile'
        verbose_name_plural = 'Extender User Profiles'

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        UProfile.objects.create(user=instance)
