from django.urls import path
from django.contrib.auth.urls import views as url_views
from . import views


urlpatterns = [
    path(
        "signup/",
        views.SignUp.as_view(),
        name="signup"
    ),

]