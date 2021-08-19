from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views

from .serializers import (
    UserSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerifyResponseSerializer,
)


class TokenObtainPairView(jwt_views.TokenObtainPairView):
    @swagger_auto_schema(responses={200: TokenObtainPairResponseSerializer()})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(jwt_views.TokenRefreshView):
    @swagger_auto_schema(responses={200: TokenRefreshResponseSerializer()})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(jwt_views.TokenVerifyView):
    @swagger_auto_schema(responses={200: TokenVerifyResponseSerializer()})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CurrentUserViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: UserSerializer()})
    def list(self, request):
        """Retrieve current user."""
        return Response(
            UserSerializer(context={"request": request}).to_representation(request.user)
        )
