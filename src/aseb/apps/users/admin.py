from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group

from aseb.apps.users.models import User
from aseb.core.admin import APIAdminModel

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, APIAdminModel):
    search_fields = ["email", "first_name", "last_name"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password", "username")}),
        (
            "Personal info",
            {"fields": (("first_name", "last_name", "avatar"),)},
        ),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Security", {"fields": ("secret_key", "jwt_jti"), "classes": "collapse"}),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    date_hierarchy = "date_joined"
    readonly_fields = ("secret_key", "jwt_jti")
