from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("api/cinema/", include("cinema.urls")),
    path("api/user/", include("user.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
