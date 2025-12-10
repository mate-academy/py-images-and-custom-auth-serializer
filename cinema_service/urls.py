from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from cinema_service import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/cinema/", include(("cinema.urls", "cinema"),
                                namespace="cinema")),
    path("api/user/", include(("user.urls", "user"), namespace="user")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
