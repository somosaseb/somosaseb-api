from django.contrib import admin

from .models import Post, Topic, Vote


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = "title", "topic", "votes", "score", "created_at", "created_by"
    list_filter = "topic", "created_by"
    date_hierarchy = "created_at"
    search_fields = ("title",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = "post", "user", "created_at"
    list_select_related = "post", "user"
