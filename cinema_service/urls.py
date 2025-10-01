from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import cinema_service.settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/cinema/", include("cinema.urls", namespace="cinema")),
    path("api/user/", include("user.urls", namespace="user")),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(
    cinema_service.settings.MEDIA_URL,
    document_root=cinema_service.settings.MEDIA_ROOT)
