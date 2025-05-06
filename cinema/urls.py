from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cinema.views import (
    ActorViewSet,
    CinemaHallViewSet,
    GenreViewSet,
    MovieViewSet,
    MovieSessionViewSet,
    OrderViewSet,
    TicketViewSet,
    MovieImageView,
)

router = DefaultRouter()
router.register("actors", ActorViewSet)
router.register("cinema_halls", CinemaHallViewSet)
router.register("genres", GenreViewSet)
router.register("movies", MovieViewSet)
router.register("movie_sessions", MovieSessionViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)

app_name = "cinema"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "movies/<int:pk>/upload-image/",
        MovieImageView.as_view(),
        name="movie-upload-image",
    ),
]
