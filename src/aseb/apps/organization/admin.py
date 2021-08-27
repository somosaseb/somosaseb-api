from django.contrib import admin

from aseb.core.admin import AdminAuditedModel, APIAdminModel

from .models import Company, Member, Topic


@admin.register(Company)
class CompanyAdmin(AdminAuditedModel):
    search_fields = "slug", "display_name"
    list_display = "__str__", "size", "created_at"
    list_filter = ("markets",)
    autocomplete_fields = "interests", "markets"


@admin.register(Topic)
class InterestAdmin(admin.ModelAdmin):
    search_fields = ("name", "emoji", "created_at")


@admin.register(Member)
class MemberAdmin(AdminAuditedModel, APIAdminModel):
    date_hierarchy = "created_at"
    list_display = "__str__", "type", "activated_at", "created_at"
    list_filter = "type", "position", "birthday"
    search_fields = "contact_email", "first_name", "last_name"
    autocomplete_fields = (
        "interests",
        "markets",
        "login",
        "company",
        "nominated_by",
        "mentor_interests",
    )
    add_fieldsets = [
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "headline",
                    "presentation",
                    "interests",
                    "markets",
                    "birthday",
                )
            },
        ),
        (
            "Membership",
            {
                "fields": [
                    "type",
                    "nominated_by",
                    "activated_at",
                ]
            },
        ),
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "display_name",
                    "headline",
                    "presentation",
                    "interests",
                    "markets",
                    "birthday",
                )
            },
        ),
        (
            "Membership",
            {
                "fields": [
                    "type",
                    "position",
                    "company",
                    "nominated_by",
                    "activated_at",
                    "expires_at",
                ]
            },
        ),
        (
            "Mentor Program",
            {
                "fields": [
                    "mentor_since",
                    "mentor_interests",
                    "mentor_presentation",
                ]
            },
        ),
        (
            "Webpage",
            {
                "fields": [
                    "title",
                    "slug",
                    "seo_title",
                    "seo_description",
                    "main_image",
                ],
                "classes": ["aside"],
            },
        ),
        (
            "Important Dates",
            {
                "fields": [
                    "created_at",
                    "created_by",
                    "modified_at",
                    "modified_by",
                ],
                "classes": ["aside"],
            },
        ),
    ]

    def get_fieldsets(self, request, obj=None):
        if obj:
            return super().get_fieldsets(request, obj)

        return self.add_fieldsets
