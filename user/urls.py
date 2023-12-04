from django.urls import path, re_path

from user.views import CreateUserView, ManageUserView, obtain_auth_token

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", obtain_auth_token, name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
