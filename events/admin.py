from django.contrib import admin
from django.http import HttpResponse
from .models import Event, Organization, EventRegistration, \
                    Project, EventClass, EventSponsorship, Idea, \
                    IdeaComment, GitHubCache
from markdownx.admin import MarkdownxModelAdmin
import csv

# Register your models here.
admin.site.register(Event, MarkdownxModelAdmin)
admin.site.register(EventClass)
admin.site.register(Organization)
admin.site.register(Project)
admin.site.register(Idea)
admin.site.register(IdeaComment)
admin.site.register(EventSponsorship)
admin.site.register(GitHubCache)

class ExportCsvMixin:
    def get_email(self, obj):
        return obj.member.email

    def get_names(self, obj):
        first = obj.member.first_name
        last = obj.member.last_name
        return  f"{first} {last}"

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        field_names = "event,member,register_date,shirt_size,diet_restriction".split(",")

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names + ["email", "full name"])
        for obj in queryset:
            lst = [getattr(obj, field) for field in field_names]
            lst += [self.get_email(obj), self.get_names(obj)]
            row = writer.writerow(lst)

        return response

    export_as_csv.short_description = "Export Selected"

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("member", "get_email", "shirt_size", "diet_restriction", "event")
    def get_email(self, obj):
        return obj.member.email
        
    get_email.admin_order_field  = 'get_email' 
    get_email.short_description = 'e-mail'
    list_filter = ("event",)
    actions = ["export_as_csv"]
