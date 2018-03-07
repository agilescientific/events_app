from django.contrib import admin
from .models import Event, Team, EventRegistration, \
                    Project, EventClass \

# Register your models here.
admin.site.register(Event)
admin.site.register(EventClass)
admin.site.register(Team)
admin.site.register(Project)
admin.site.register(EventRegistration)