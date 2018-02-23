from django.db import models


class Event(models.Model):
    event_title = models.CharField(max_length=100)
    description_text = models.TextField(max_length=300)
    img_url = models.CharField(max_length=200, default="http://placehold.it/700x300")
    event_date = models.DateField('event date')
    event_time = models.CharField(max_length=50)
    event_location = models.CharField(max_length=100)

    def __str__(self):
        return self.event_title
    

class Detail(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    body_text = models.TextField(max_length=500)
