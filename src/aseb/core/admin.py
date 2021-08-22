from django.contrib import admin
from django.forms import forms


class AdminSite(admin.AdminSite):
    enable_nav_sidebar = False

    def each_context(self, request):
        js = [
            "vendor/jquery/jquery.min.js",
            "jquery.init.js",
        ]
        media = forms.Media(js=["admin/js/%s" % url for url in js])

        return {
            **super().each_context(request),
            "media": media,
        }


class AdminAuditedModel(admin.ModelAdmin):
    readonly_fields = "created_at", "created_by", "modified_at", "modified_by"

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)
