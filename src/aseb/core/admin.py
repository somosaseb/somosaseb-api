from django.contrib import admin
from django.contrib.admin.utils import lookup_field
from django.contrib.admin.views import main as admin_main_views
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import ObjectDoesNotExist
from django.forms import forms
from django.http import HttpRequest, JsonResponse
from rest_framework.utils.mediatypes import media_type_matches


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


# Monkey way to allow a new parameter to the changelist view ¯\_(ツ)_/¯
admin_main_views.IGNORED_PARAMS = [
    "format",
    *admin_main_views.IGNORED_PARAMS,
]


def is_api_list(request: HttpRequest):
    if request.method != "GET":
        return False

    return request.GET.get("format", "") == "json" or media_type_matches(
        "application/json",
        request.content_type,
    )


def serialize_items(
    cl: ChangeList,
):
    def iterator(result):
        for field_name in cl.list_display:
            if field_name == "action_checkbox":
                continue

            try:
                f, attr, value = lookup_field(field_name, result, cl.model_admin)
            except ObjectDoesNotExist:
                yield field_name, None
            else:
                if f is None or f.auto_created:
                    result_repr = repr(value)
                else:
                    result_repr = value

                yield field_name, result_repr

    return [{name: value for name, value in iterator(res)} for res in cl.result_list]


class APIAdminModel(admin.ModelAdmin):
    def changelist_view(self, request: HttpRequest, extra_context=None):
        response = super().changelist_view(request, extra_context)

        if is_api_list(request):
            changelist = response.context_data["cl"]

            return JsonResponse(
                {
                    "results": serialize_items(changelist),
                    "page": changelist.page_num,
                    "per_page": changelist.paginator.per_page,
                    "count": changelist.paginator.count,
                }
            )

        return response
