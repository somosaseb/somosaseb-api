from django.contrib.admin.apps import AdminConfig


class CoreConfig(AdminConfig):
    default_site = "aseb.core.admin.AdminSite"
