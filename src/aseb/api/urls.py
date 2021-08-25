from .auth.viewsets import AuthViewSet
from .members.viewsets import MemberViewSet
from .router import Router
from .users.viewsets import CurrentUserViewSet

router = Router()

router.register("me", CurrentUserViewSet, basename="api-me")
router.register("members", MemberViewSet, basename="member")
router.register("auth", AuthViewSet, basename="auth")

urlpatterns = [
    *router.urls,
]
