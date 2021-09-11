from aseb.api import viewsets
from aseb.apps.pages.models import Page
from rest_framework import serializers


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ("path", "slug", "title", "content")


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    model = Page
    serializer_class = PageSerializer

    def get_queryset(self):
        return Page.objects.for_request(self.request)
