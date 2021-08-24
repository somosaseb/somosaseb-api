from django.conf import settings
from django.urls.conf import path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework.routers import Route


class Router(routers.DefaultRouter):
    include_root_view = False
    include_format_suffixes = False

    routes = [
        Route(
            url=r"^{prefix}/count{trailing_slash}$",
            mapping={"get": "count"},
            name="{basename}-count",
            detail=False,
            initkwargs={"suffix": "Count"},
        ),
        *routers.DefaultRouter.routes,
    ]

    def get_urls(self):
        urlpatterns = super().get_urls()

        schema_view = get_schema_view(
            openapi.Info(
                title="ASEB API",
                default_version="v1",
            ),
            public=True,
            permission_classes=(
                permissions.AllowAny if settings.DEBUG else permissions.IsAuthenticated,
            ),
        )

        swagger_schema = schema_view.without_ui(cache_timeout=0)

        return [
            path("", TemplateView.as_view(template_name="api/docs.html"), name="root-view"),
            path("schema.json", swagger_schema, name="schema"),
            *urlpatterns,
        ]
