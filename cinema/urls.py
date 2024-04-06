from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import routers
import cinema_service

from cinema.views import (
    GenreViewSet,
    ActorViewSet,
    CinemaHallViewSet,
    MovieViewSet,
    MovieSessionViewSet,
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
    path("", include(router.urls))
] + static(
    cinema_service.settings.MEDIA_URL,
    document_root=cinema_service.settings.MEDIA_ROOT
)

app_name = "cinema"
