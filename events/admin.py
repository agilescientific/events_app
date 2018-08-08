from django.contrib import admin
from .models import Event, Organization, EventRegistration, \
                    Project, EventClass, EventSponsorship, Idea, \
                    IdeaComment
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
admin.site.register(Event, MarkdownxModelAdmin)
admin.site.register(EventClass)
admin.site.register(Organization)
admin.site.register(Project)
admin.site.register(Idea)
admin.site.register(IdeaComment)
admin.site.register(EventRegistration)
admin.site.register(EventSponsorship)