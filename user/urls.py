from django.urls import path

from user.views import CreateUserList, LoginUserView, UserDetail

app_name = "user"

urlpatterns = [
    path("register/", CreateUserList.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", UserDetail.as_view(), name="manage"),
]
