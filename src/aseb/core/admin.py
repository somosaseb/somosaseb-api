from functools import update_wrapper
from inspect import getmembers

from django.contrib import admin
from django.contrib.admin.utils import lookup_field, unquote
from django.contrib.admin.views import main as admin_main_views
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.forms import forms
from django.http import HttpRequest, JsonResponse
from django.urls import path
from django.utils.text import capfirst
from rest_framework.viewsets import ViewSetMixin, _check_attr_name

from aseb.core.utils import request_json_response


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

    return request_json_response(request)


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


def adminaction(detail: bool = None, **kwargs):
    assert detail is not None, "@action() missing required argument: 'detail'"

    def decorator(func):
        func.url_name = func.__name__.replace("_", "-")
        func.detail = detail
        func.kwargs = kwargs
        return func

    return decorator


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

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urlpatterns = super().get_urls()
        extra_actions = getmembers(self.__class__, lambda prop: hasattr(prop, "detail"))
        extra_actions = [method for name, method in extra_actions]

        for action_view in extra_actions:
            if action_view.detail:
                urlpatterns.insert(
                    2,  # Just before the history view
                    path(
                        f"<path:object_id>/{action_view.url_name}/",
                        wrap(self.detail_view),
                        {"action_view": action_view},
                        name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_{action_view.url_name}",
                    ),
                )

        return urlpatterns

    def detail_view(self, request, object_id, action_view):
        opts = self.model._meta
        app_label = opts.app_label
        object_name = str(opts.verbose_name)
        obj = self.get_object(request, unquote(object_id))

        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        if not self.has_view_or_change_permission(request, obj):
            raise PermissionDenied
        context = {
            **self.admin_site.each_context(request),
            "object_id": object_id,
            "object": obj,
            "object_name": object_name,
            "opts": opts,
            "app_label": app_label,
            "module_name": str(capfirst(opts.verbose_name_plural)),
        }
        return action_view(self, request, obj, context)
