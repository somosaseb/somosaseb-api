from django.urls import path

from .router import Router
from .users.viewsets import (
    CurrentUserViewSet,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = Router()

router.register("me", CurrentUserViewSet, basename="api-me")


urlpatterns = [
    *router.urls,
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
