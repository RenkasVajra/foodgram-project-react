from django.urls import path
from django.contrib.auth.urls import views as url_views
from . import views


urlpatterns = [
    path(
        "signup/",
        views.SignUp.as_view(),
        name="signup"
    ),

    path(
        "password_change",
        url_views.PasswordChangeView.as_view(),
        name="password_change"
    ),
    path(
        "password_change/done",
        url_views.PasswordChangeDoneView.as_view(),
        name="password_change_done"
    ),

    path(
        "password_reset",
        url_views.PasswordResetView.as_view(),
        name="password_reset"
    ),
    path(
        "password_reset/done",
        url_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>",
        url_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),
    path(
        "reset/done",
        url_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"
    )
]
