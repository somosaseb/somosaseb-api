from .auth.viewsets import AuthViewSet
from .members.viewsets import MemberViewSet
from .router import Router
from .topics.viewsets import TopicViewSet
from .users.viewsets import CurrentUserViewSet

router = Router()

router.register("me", CurrentUserViewSet, basename="api-me")
router.register("auth", AuthViewSet, basename="auth")
router.register("members", MemberViewSet, basename="member")
router.register("topics", TopicViewSet, basename="topic")

urlpatterns = [
    *router.urls,
]
