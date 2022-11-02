from django.urls import path
from user.views import login, signup, signout

urlpatterns = [
    path("login/", login),
    path("signup/", signup),
    path("signout/", signout),
]
