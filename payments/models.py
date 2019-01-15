from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from markdownx.models import MarkdownxField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager

User = get_user_model()

class Amount(models.Model):
    event = models.ForeignKey('events.Event', related_name='payment_amount_info', on_delete=models.CASCADE)
    amount = models.FloatField()
    currency = models.CharField(max_length=20, verbose_name="Currency (3 char)")
    description = models.CharField(max_length=200)
    long_description = MarkdownxField(max_length=1000, default="", verbose_name='Elaborate description (payment screen)')
    img_url = models.URLField(verbose_name="URL for payment image", default="https://placeimg.com/640/480/any")

    def __str__(self):
        return self.event.event_title + " - " + str(self.amount) + " " + self.currency

class Payment(models.Model):
    event = models.ForeignKey('events.Event', related_name='payment_event_info', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='payment_user_info', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    stripe_id = models.CharField(max_length=100)
    amount = models.ForeignKey(Amount, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username + " - " + self.event.event_title

