from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from aseb.api import viewsets

from ..users.serializers import UserSerializer
from .serializers import RegisterSerializer


class AuthViewSet(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        tags=["auth"],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
            )
        },
    )
    @action(methods=["post"], detail=False)
    def register(self, request, **kwargs):
        serializer = RegisterSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(UserSerializer(context={"request": request}).to_representation(user))
