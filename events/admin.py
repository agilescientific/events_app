from django.contrib import admin
from .models import Event, Team, EventRegistration

# Register your models here.
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(EventRegistration)