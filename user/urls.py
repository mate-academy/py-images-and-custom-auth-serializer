from django.urls import path
from user.views import CreateUserView, MyAuthToken, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", MyAuthToken.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
