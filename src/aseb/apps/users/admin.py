from typing import Any, Dict

from django.contrib import admin, messages
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm
from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from aseb.apps.organization.models import Member
from aseb.apps.users.models import User
from aseb.core.admin import APIAdminModel, adminaction

admin.site.unregister(Group)


class UserChangeForm(auth_admin.UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a> or '
            'Or reset <a href="../reset-password/">Send a reset link</a>.'
        ),
    )


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, APIAdminModel):
    class MembershipInline(admin.StackedInline):
        verbose_name = "Membership"
        model = Member
        fk_name = "login"
        fields = ("type", "birthday", "visibility")
        can_delete = False
        extra = 0
        max_num = 1

    form = UserChangeForm
    inlines = [MembershipInline]
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
        ("Security", {"fields": ("secret_key",), "classes": "collapse"}),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "last_login",
    )
    date_hierarchy = "date_joined"
    readonly_fields = ("secret_key", "jwt_jti")

    def get_inlines(self, request: HttpRequest, obj):
        if not obj:
            return []

        return super().get_inlines(request, obj)

    @adminaction(detail=True)
    def reset_password(
        self,
        request: HttpRequest,
        obj: User,
        context: Dict[str, Any],
        **kwargs,
    ):

        if request.POST:
            form = PasswordResetForm(data={"email": obj.email})
            form.is_valid()
            form.save(
                domain_override=request.get_host(),
                use_https=request.get_port() == 443,
            )

            messages.success(request, f"Reset password sent to {obj}")
            return redirect(request.path)

        return render(
            request,
            "admin/user/action_reset_password.html",
            {**context, "title": "Reset password"},
        )
