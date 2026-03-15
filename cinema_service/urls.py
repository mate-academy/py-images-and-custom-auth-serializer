from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/cinema/",
        include(("cinema.urls", "cinema"), namespace="cinema"),
    ),
    path(
        "api/user/",
        include(("user.urls", "user"), namespace="user"),
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]

# ✅ Serve media files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
