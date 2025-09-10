from django.conf import settings
from django.conf.urls.static import static
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
router.register("movies", MovieViewSet)
router.register("movie_sessions", MovieSessionViewSet)
router.register("orders", OrderViewSet)

movie_upload = MovieViewSet.as_view({"post": "upload_image"})


urlpatterns = [
    path("", include(router.urls)),
    path("upload-image/", movie_upload, name="movie-upload-image")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "cinema"
