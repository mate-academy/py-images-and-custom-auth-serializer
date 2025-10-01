from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

from cinema.views import (
    ActorViewSet,
    CinemaHallViewSet,
    GenreViewSet,
    MovieSessionViewSet,
    MovieViewSet,
    OrderViewSet,
)

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("cinema_halls", CinemaHallViewSet)
router.register("movies", MovieViewSet)
router.register("movie_sessions", MovieSessionViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    # expõe as rotas do DRF com namespace "cinema"
    path("", include(("cinema.urls", "cinema"), namespace="cinema")),
    path("api/cinema/", include(router.urls)),
    path("api/user/", include(("user.urls", "user"), namespace="user")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(
            "__debug__/",
            include(debug_toolbar.urls),
        ),
    ]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
