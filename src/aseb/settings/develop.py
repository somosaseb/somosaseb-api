from .base import *  # noqa:

DEBUG = True

INTERNAL_IPS = []
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    *INSTALLED_APPS,  # noqa:
    "debug_toolbar",
]

MIDDLEWARE = [
    *MIDDLEWARE,  # noqa:
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

SWAGGER_SETTINGS["OAUTH2_CONFIG"]["clientId"] = "CLIENT_ID"  # noqa:
SWAGGER_SETTINGS["OAUTH2_CONFIG"]["clientSecret"] = "CLIENT_SECRET"  # noqa:
SWAGGER_SETTINGS[  # noqa:
    "OAUTH2_REDIRECT_URL"
] = "http://localhost:8000/static/drf-yasg/swagger-ui-dist/oauth2-redirect.html"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
    "SHOW_TOOLBAR_CALLBACK": lambda request: not request.is_ajax(),
}

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
]
