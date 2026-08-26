from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from cinema_service.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/cinema/", include("cinema.urls", namespace="cinema")),
    path("api/user/", include("user.urls", namespace="user")),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
