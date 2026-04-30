from django.urls import path, include
from rest_framework import routers

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

# Add basename="movie" to match the test requirements
router.register("movies", MovieViewSet, basename="movie")

# Add basename="moviesession" for consistency
router.register("movie_sessions", MovieSessionViewSet, basename="moviesession")

router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "cinema"
