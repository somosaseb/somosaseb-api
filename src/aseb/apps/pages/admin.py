from django.contrib import admin
from .models import Page, Website


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "created_at", "published_at")
    search_fields = ("path", "title")


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "root_page", "reader_access", "created_at")
    search_fields = ("name",)
    autocomplete_fields = ["root_page"]
