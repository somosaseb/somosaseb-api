from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    search_fields = ["email", "first_name", "last_name"]
    fieldsets = (
        (None, {"fields": ("email", "password", "username")}),
        (
            "Personal info",
            {"fields": (("first_name", "last_name"),)},
        ),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        (None, {"fields": ("secret_key",)}),
    )

    list_display = (
        "__str__",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    date_hierarchy = "date_joined"
    readonly_fields = ("secret_key",)
