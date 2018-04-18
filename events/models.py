from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
User = get_user_model()

class EventClass(models.Model):
    e_class = models.CharField(max_length=100)

    def __str__(self):
        return self.e_class
    
    class Meta:
        verbose_name_plural = "Event Classes"

class Event(models.Model):
    event_title = models.CharField(max_length=100)
    description_text = models.TextField(max_length=300)
    img_url = models.CharField(max_length=200, default="http://placehold.it/700x300")
    event_date = models.DateField('event date')
    event_time = models.CharField(max_length=50)
    event_location = models.CharField(max_length=100)
    body_text = models.TextField(max_length=500, default="")
    event_class = models.ForeignKey(EventClass, on_delete=models.CASCADE)
    forum = models.ForeignKey('forum.Forum', related_name='event_forum',
                              on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.event_title

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this event.
        """
        return reverse('event-detail', args=[str(self.id)])

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, related_name='event_info', on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name='user_info', on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member.username + " - " + self.event.event_title


class Team(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)
    leader = models.ForeignKey(User, related_name='teamleader', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " - " + self.event.event_title

    def get_absolute_url(self):
        """
        Returns the url to access a particular team instance.
        """
        return reverse('team-detail', args=[str(self.id)])

class Project(models.Model):
    name = models.CharField(max_length=100)
    detail_small = models.TextField(max_length=500, default="", verbose_name='Description')
    detail_long = models.TextField(max_length=1000, default="", verbose_name='Long Description')
    main_url = models.CharField(max_length=100, default='')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='projectCreator', on_delete=models.CASCADE)
    votes = models.BigIntegerField(default=0)
    github = models.URLField(verbose_name='URL to Github Repo')
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name + " - " + self.event.event_title

    def get_absolute_url(self):
        """
        Returns the url to access a particular team instance.
        """
        return reverse('project-detail', args=[str(self.id)])
