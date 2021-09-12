from django.contrib.auth import views
from django.urls import path
from aseb.apps.users.views import RegisterView

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
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
