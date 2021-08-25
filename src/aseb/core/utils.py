from django.http import HttpRequest
from rest_framework.utils.mediatypes import media_type_matches


def request_json_response(request: HttpRequest) -> bool:
    return request.GET.get("format", "") == "json" or media_type_matches(
        "application/json",
        request.content_type,
    )
