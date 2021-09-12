from django.urls import re_path

from .auth.viewsets import AuthViewSet
from .members.viewsets import MemberViewSet
from .oauth.viewsets import (
    AuthorizationView,
    AuthorizedTokenDeleteView,
    AuthorizedTokensListView,
    IntrospectTokenView,
    RevokeTokenView,
    TokenView,
)
from .pages.viewsets import PageViewSet
from .router import Router
from .topics.viewsets import TopicViewSet
from .users.viewsets import CurrentUserViewSet

router = Router()

router.register("me", CurrentUserViewSet, basename="api-me")
router.register("auth", AuthViewSet, basename="auth")
router.register("members", MemberViewSet, basename="member")
router.register("topics", TopicViewSet, basename="topic")
router.register("pages", PageViewSet, basename="page")

urlpatterns = [*router.urls]

oauth2_urlpatterns = [
    re_path(r"^oauth/authorize/$", AuthorizationView.as_view(), name="authorize"),
    re_path(r"^oauth/token/$", TokenView.as_view(), name="token"),
    re_path(r"^oauth/revoke_token/$", RevokeTokenView.as_view(), name="revoke-token"),
    re_path(r"^oauth/introspect/$", IntrospectTokenView.as_view(), name="introspect"),
    re_path(
        r"^oauth/authorized-tokens/$",
        AuthorizedTokensListView.as_view(),
        name="authorized-token-list",
    ),
    re_path(
        r"^oauth/authorized-tokens/(?P<pk>[\w-]+)/delete/$",
        AuthorizedTokenDeleteView.as_view(),
        name="authorized-token-delete",
    ),
]
