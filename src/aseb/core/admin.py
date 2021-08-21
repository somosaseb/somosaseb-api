from django.contrib import admin


class AdminSite(admin.AdminSite):
    enable_nav_sidebar = False


class AdminAuditedModel(admin.ModelAdmin):
    readonly_fields = "created_at", "created_by", "modified_at", "modified_by"

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)
