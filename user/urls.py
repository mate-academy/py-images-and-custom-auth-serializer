from django.urls import path
from user.views import CreateUserView, CustomObtainAuthToken, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CustomObtainAuthToken.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
