from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cinema.models import Movie, Genre, Actor, CinemaHall, MovieSession, Order
from cinema.permissions import IsAdminOrIfAuthenticatedReadOnly, IsAuthenticatedOrAdmin
from cinema.serializers import (
    MovieSerializer,
    GenreSerializer,
    ActorSerializer,
    CinemaHallSerializer, MovieSessionSerializer, OrderSerializer, MovieListSerializer, MovieRetrieveSerializer,
    MovieSessionRetrieveSerializer, MovieImageSerializer,
)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    http_method_names = ["get", "post"]

    @staticmethod
    def _params_to_ints(qs):
        """Convert a string of format '1, 2, 3' to a list of integers [1, 2, 3]."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieRetrieveSerializer
        elif self.action == "upload_image":
            return MovieImageSerializer
        return MovieSerializer

    def get_queryset(self):
        queryset = self.queryset
        actors = self.request.query_params.get("actors")
        genres = self.request.query_params.get("genres")
        title = self.request.query_params.get("title")

        if actors:
            actors = self._params_to_ints(actors)
            queryset = queryset.filter(actors__id__in=actors)
        if genres:
            genres = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genres)

        if title:
            queryset = queryset.filter(title__icontains=title)


        queryset = queryset.distinct()
        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("genres", "actors")

        return queryset

    @action(
        methods=["GET", "POST"],
        detail=True,
        permission_classes=(IsAdminOrIfAuthenticatedReadOnly,), #not necessary
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    http_method_names = ["get", "post"]


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    http_method_names = ["get", "post"]


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    http_method_names = ["get", "post"]


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrAdmin,)
    http_method_names = ["get", "post"]

    @staticmethod
    def _params_to_ints(qs):
        """Convert a string of format '1, 2, 3' to a list of integers [1, 2, 3]."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSessionSerializer
        elif self.action == "retrieve":
            return MovieSessionRetrieveSerializer
        elif self.action == "upload_image":
            return MovieImageSerializer
        return MovieSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        date = self.request.query_params.get("date")
        movie = self.request.query_params.get("movie")

        if date:
            queryset = queryset.filter(show_time__date=date)

        if movie:
            movie = self._params_to_ints(movie)
            queryset = queryset.filter(movie__id__in=movie)

        if self.action in ("retrieve",):
            return queryset.select_related("movie", "cinema_hall")

        return queryset

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=(IsAdminOrIfAuthenticatedReadOnly,),  # not necessary
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        movie_session = self.get_object()
        serializer = self.get_serializer(movie_session, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post"]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.action == "list":
            queryset = queryset.prefetch_related("tickets__movie_session__cinema_hall")

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
