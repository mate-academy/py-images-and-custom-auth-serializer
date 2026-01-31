from django.urls import path

from user.views import LoginView, ManageUserView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("me/", ManageUserView.as_view(), name="user-me"),
]
