import os
import django
from datetime import datetime
from django.core.handlers.wsgi import WSGIHandler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aseb.settings.develop")


class WSGIApplication(WSGIHandler):
    def __init__(self, *args, **kwargs):
        django.setup(set_prefix=False)
        os.environ.setdefault("DEPLOY_VERSION", "develop")
        os.environ.setdefault("DEPLOY_DATETIME", datetime.utcnow().isoformat())

        deploy_version = os.environ.get("DEPLOY_VERSION")
        deploy_datetime = os.environ.get("DEPLOY_DATETIME")

        self.served_by = "rev={};date={}".format(deploy_version, deploy_datetime)

        super().__init__(*args, **kwargs)

    def get_response(self, request):
        response = super().get_response(request)
        response["X-Served-By"] = self.served_by

        return response


def get_wsgi_application():
    django.setup(set_prefix=False)
    return WSGIApplication()


application = get_wsgi_application()
