from typing import Dict, Type

from rest_framework import generics, mixins, serializers, viewsets
from rest_framework.viewsets import ViewSetMixin

from aseb.api.mixins import CountModelMixin
from aseb.core.exceptions import ResponseException


class GenericAPIView(generics.GenericAPIView):
    def handle_exception(self, exc):
        if isinstance(exc, ResponseException):
            return exc.response

        return super().handle_exception(exc)


class GenericViewSet(ViewSetMixin, GenericAPIView):
    serializers_classes: Dict[str, Type[serializers.Serializer]] = {}

    def get_serializer_class(self):
        return self.serializers_classes.get(
            self.action,
            super().get_serializer_class(),
        )


class ViewSet(viewsets.ViewSet):
    ...


class ReadOnlyModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    CountModelMixin,
    GenericViewSet,
):
    ...


class ModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    CountModelMixin,
    GenericViewSet,
):
    ...
