from django.contrib.auth import views
from django.urls import path, re_path

from .views import (
    AuthorizationView,
    IntrospectTokenView,
    RevokeTokenView,
    TokenView,
    AuthorizedTokenDeleteView,
    AuthorizedTokensListView,
)

urlpatterns = [
    path(
        "password_reset/",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
