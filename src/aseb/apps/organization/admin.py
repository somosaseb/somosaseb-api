from django.contrib import admin

from .models import Company, Interest, Market, Member


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("title", "slug")


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    autocomplete_fields = ("sibling",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ("contact_email", "first_name", "last_name")
    autocomplete_fields = (
        "interests",
        "markets",
        "login",
        "company",
        "nominated_by",
        "mentor_interests",
    )
