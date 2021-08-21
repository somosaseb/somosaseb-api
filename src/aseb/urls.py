from functools import partial

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path("admin/docs/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("aseb.api.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    serve_with_indexes = partial(serve, show_indexes=True)
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        *static(
            prefix=settings.STATIC_URL,
            view=serve_with_indexes,
            document_root=settings.STATIC_ROOT,
        ),
        *static(
            prefix=settings.MEDIA_URL,
            view=serve_with_indexes,
            document_root=settings.MEDIA_ROOT,
        ),
        *urlpatterns,
    ]
