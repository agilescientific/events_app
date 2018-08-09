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

def logo_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/org<slug>/<filename>
    return '{0}/{1}'.format(instance.slug, filename)

class EventClass(models.Model):
    e_class = models.CharField(max_length=100)

    def __str__(self):
        return self.e_class
    
    class Meta:
        verbose_name_plural = "Event Classes"

class Organization(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, blank=True)
    leader = models.ForeignKey(User, related_name='organizationleader', on_delete=models.CASCADE)
    website = models.URLField(verbose_name='Website URL')
    linkedin_uname = models.CharField(max_length=50, null=True, blank=True)

    org_logo = models.ImageField(upload_to=logo_directory_path,  null=True, blank=True,
                                    default='default/blank-profile.png')
    org_logo_thumbnail = ImageSpecField(source='org_logo',
                                      format='JPEG',
                                      options={'quality': 90})

    slug = models.SlugField(max_length=140, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular team instance.
        """
        return reverse('organization-detail', args=[str(self.slug)])

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Organization.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

class Event(models.Model):
    event_title = models.CharField(max_length=100)
    description_text = models.TextField(max_length=300)
    img_url = models.CharField(max_length=200, default="http://placehold.it/700x300")
    event_startdate = models.DateTimeField('event start', null=True)
    event_enddate = models.DateTimeField('event end', null=True)
    event_location_name = models.CharField(max_length=100, null=True)
    event_location_address = models.CharField(max_length=100, null=True)
    event_location_city = models.CharField(max_length=100, null=True)
    event_location_country = models.CharField(max_length=100, null=True)

    body_text = MarkdownxField(max_length=5000, default="")
    rules = MarkdownxField(max_length = 10000, default="")
    event_class = models.ForeignKey(EventClass, on_delete=models.CASCADE)
    forum = models.ForeignKey('forum.Forum', related_name='event_forum',
                              on_delete=models.CASCADE, blank=True, null=True)

    sponsors = models.ManyToManyField('EventSponsorship', related_name="sponsor_list", blank=True)

    banner_img = models.ImageField(upload_to=logo_directory_path,  null=True, blank=True,
                                    default='http://placehold.it/1000x300')

    slug = models.SlugField(max_length=140, null=True)
    need_ideas = models.NullBooleanField()
    canjoin = models.NullBooleanField()
    hide = models.NullBooleanField()

    slack_webhook = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.event_title

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this event.
        """
        return reverse('event-detail', args=[self.slug])

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Event.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

class EventSponsorship(models.Model):
    event = models.ForeignKey(Event, related_name='event_esponsored', on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Organization, related_name='sponsor_info', on_delete=models.CASCADE)
    tier = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    amount = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.sponsor.name + " - " + self.event.event_title

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, related_name='event_info', on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name='user_info', on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member.username + " - " + self.event.event_title

class Project(models.Model):
    name = models.CharField(max_length=100)
    detail_small = models.TextField(max_length=200, default="", verbose_name='Description')
    detail_long = MarkdownxField(max_length=2000, default="", verbose_name='Long Description')
    main_url = models.CharField(max_length=100, default='', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='projectCreator', on_delete=models.CASCADE)
    votes = models.BigIntegerField(default=0)
    github = models.URLField(verbose_name='URL to Github Repo', null=True, blank=True)
    members = models.ManyToManyField(User, blank=True)
    slug = models.SlugField(max_length=140, null=True)
    resources = TaggableManager(verbose_name='Resources', blank=True)

    def __str__(self):
        return self.name + " - " + self.event.event_title

    def get_absolute_url(self):
        """
        Returns the url to access a particular team instance.
        """
        return reverse('project-detail', args=[str(self.slug)])

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Project.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

class IdeaComment(models.Model):
    parentIdea = models.ForeignKey('Idea', on_delete=models.CASCADE)
    content = MarkdownxField(max_length=500, default="", verbose_name='Comment')
    author = models.ForeignKey(User, related_name='commentAuthor', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='commentEvent', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.parentIdea.name + " - " + self.event.event_title

class Idea(models.Model):
    name = models.CharField(max_length=100)
    detail_short = models.CharField(max_length=200, default="", verbose_name='Short description')
    detail = MarkdownxField(max_length=500, default="", verbose_name='Description')
    main_url = models.CharField(max_length=100, default='', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='ideaCreator', on_delete=models.CASCADE)
    votes = models.BigIntegerField(default=0, blank=True)
    voters = models.ManyToManyField(User, blank=True)
    slug = models.SlugField(max_length=140, null=True)
    tags = TaggableManager(verbose_name='ideaTags', blank=True)
    comments = models.ManyToManyField(IdeaComment, blank=True)

    def __str__(self):
        return self.name + " - " + self.event.event_title

    def get_absolute_url(self):
        """
        Returns the url to access a particular team instance.
        """
        return reverse('idea-detail', args=[str(self.slug)])

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Idea.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()
