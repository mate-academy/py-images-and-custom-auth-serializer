from django.urls import path, include
from rest_framework import routers

from cinema.views import (
    GenreViewSet,
    ActorViewSet,
    CinemaHallViewSet,
    MovieViewSet,
    MovieSessionViewSet,
    OrderViewSet,
    MovieImageUploadView,
)

from .views import MovieDetailView

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("cinema_halls", CinemaHallViewSet)
router.register("movies", MovieViewSet)
router.register("movie_sessions", MovieSessionViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("movie/<int:id>/upload-image/",
         MovieImageUploadView.as_view(),
         name="movie-upload-image"),
]

app_name = "cinema"
