from django.http import HttpResponse


class ResponseException(Exception):
    def __init__(self, response: HttpResponse, exc=None):
        self.response = response
        self.exc = exc
