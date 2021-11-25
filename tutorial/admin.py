from django.contrib import admin
from apps.events.models import EventModel


class AuthorAdmin(admin.ModelAdmin):
    pass


class EventAdmin:
    pass


admin.site.register(EventModel, EventAdmin)
