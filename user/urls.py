from django.urls import path
from user.views import (CreateUserView,
                        CreateTokenView,
                        ManageUserView,
                        CustomObtainAuthToken
                        )

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("token/", CustomObtainAuthToken.as_view(), name="custom-token"),
]
