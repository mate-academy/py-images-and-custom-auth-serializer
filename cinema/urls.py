from django.urls import path, include
from rest_framework import routers

from cinema.views import (
    GenreViewSet,
    ActorViewSet,
    CinemaHallViewSet,
    MovieViewSet,
    MovieSessionViewSet,
    OrderViewSet,
    MovieImageUploadView,  # Import da nova View
)

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("cinema_halls", CinemaHallViewSet)
router.register("movies", MovieViewSet)
router.register("movie_sessions", MovieSessionViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    # Rota para o endpoint de upload de imagem
    # Nota: A view que adicionei (MovieImageUploadView) espera 'movie_id' na URL
    path("upload-image/<int:movie_id>/", MovieImageUploadView.as_view(), name="movie-image-upload"),

    # Rotas dos ViewSets
    path("", include(router.urls))
]

app_name = "cinema"
