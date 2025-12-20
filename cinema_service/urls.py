from django.urls import path
from cinema.views import CreateTokenView

urlpatterns = [
    # ... register/me endpoints ...
    path("login/", CreateTokenView.as_view(), name="token"),
]
