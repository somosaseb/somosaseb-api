from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig as BaseAdminConfig


class CoreConfig(AppConfig):
    name = "aseb.core"


class AdminConfig(BaseAdminConfig):
    default_site = "aseb.core.admin.AdminSite"
