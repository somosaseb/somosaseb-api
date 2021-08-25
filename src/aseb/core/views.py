from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.defaults import page_not_found

from aseb.core.utils import request_json_response


def not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    if request_json_response(request):
        exception_repr = exception.__class__.__name__

        try:
            message = exception.args[0]
        except (AttributeError, IndexError):
            pass
        else:
            if isinstance(message, str):
                exception_repr = message

        return JsonResponse({"message": exception_repr})

    return page_not_found(request, exception)
