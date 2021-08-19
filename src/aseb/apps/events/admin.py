from django.contrib import admin

from .models import Event, Serie


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    search_fields = ("title", "slug")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ("title", "slug")
