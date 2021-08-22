from rest_framework import viewsets, mixins
from rest_framework.response import Response


class ViewSet(viewsets.ViewSet):
    ...


class CountModelMixin(mixins.ListModelMixin):
    def count(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        return Response({"count": count})


class ModelViewSet(
    viewsets.ModelViewSet,
    CountModelMixin,
):
    ...
