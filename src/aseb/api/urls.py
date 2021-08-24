from .members.viewsets import MemberViewSet
from .router import Router
from .users.viewsets import AuthToken, CurrentUserViewSet

router = Router()

router.register("me", CurrentUserViewSet, basename="api-me")
router.register("members", MemberViewSet, basename="user")
router.register("auth", AuthToken, basename="tokens")

urlpatterns = [
    *router.urls,
]
