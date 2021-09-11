from django.contrib.auth import views
from django.urls import path, re_path
from oauth2_provider.views import AuthorizedTokensListView, AuthorizedTokenDeleteView
from oauth2_provider.urls import base_urlpatterns as oauth2_urlpatterns

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
    *oauth2_urlpatterns,
    re_path(
        r"^authorized_tokens/$",
        AuthorizedTokensListView.as_view(),
        name="authorized-token-list",
    ),
    re_path(
        r"^authorized_tokens/(?P<pk>[\w-]+)/delete/$",
        AuthorizedTokenDeleteView.as_view(),
        name="authorized-token-delete",
    ),
]
