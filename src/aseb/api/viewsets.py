from typing import Dict, Type

from rest_framework import mixins, serializers, viewsets

from aseb.api.mixins import CountModelMixin


class GenericViewSet(viewsets.GenericViewSet):
    serializers_classes: Dict[str, Type[serializers.Serializer]] = {}

    def get_serializer_class(self):
        return self.serializers_classes.get(
            self.action,
            super().get_serializer_class(),
        )


class ViewSet(viewsets.ViewSet):
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
