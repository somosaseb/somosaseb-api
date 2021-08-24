from .members.viewsets import MemberViewSet
from .router import Router
from .users.viewsets import CurrentUserViewSet
from .auth.viewsets import AuthViewSet

router = Router()

router.register("me", CurrentUserViewSet, basename="api-me")
router.register("members", MemberViewSet, basename="user")
router.register("auth", AuthViewSet, basename="auth")

urlpatterns = [
    *router.urls,
]
