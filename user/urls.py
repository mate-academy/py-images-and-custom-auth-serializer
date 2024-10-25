from django.urls import path
from user.views import CreateUserView, CreateTokenView, ManageUserView
from django.conf import settings
from django.conf.urls.static import static

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
