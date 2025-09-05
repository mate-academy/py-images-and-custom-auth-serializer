from datetime import datetime
from django.db.models import F, Count
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date

from rest_framework import status, viewsets, mixins, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination

from cinema.models import Genre, Actor, CinemaHall, Movie, MovieSession, Order
from cinema.permissions import IsAdminOrIfAuthenticatedReadOnly
from cinema.serializers import (
    GenreSerializer,
    ActorSerializer,
    CinemaHallSerializer,
    MovieSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    MovieSessionSerializer,
    MovieSessionListSerializer,
    MovieSessionDetailSerializer,
    OrderSerializer,
    OrderListSerializer,
    MovieImageUploadSerializer,
)


# 🎬 Movie Image Upload
class MovieImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def post(self, request, pk):
        movie = get_object_or_404(Movie, id=pk)
        serializer = MovieImageUploadSerializer(
            movie, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 📚 Base ViewSet for Create + List
class BaseCreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class GenreViewSet(BaseCreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(BaseCreateListViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CinemaHallViewSet(BaseCreateListViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


# 🎥 Movie ViewSet
class MovieViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.prefetch_related("genres", "actors")
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def _params_to_ints(self, qs):
        return [int(x) for x in qs.split(",") if x.isdigit()]

    def get_queryset(self):
        qs = self.queryset
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        if title:
            qs = qs.filter(title__icontains=title)
        if genres:
            qs = qs.filter(genres__id__in=self._params_to_ints(genres))
        if actors:
            qs = qs.filter(actors__id__in=self._params_to_ints(actors))

        return qs.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        if self.action == "retrieve":
            return MovieDetailSerializer
        if self.action == "create":

            class MovieCreateSerializer(serializers.ModelSerializer):
                class Meta:
                    model = Movie
                    fields = (
                        "id",
                        "title",
                        "description",
                        "duration",
                        "genres",
                        "actors",
                    )

            return MovieCreateSerializer
        return MovieSerializer


# 🕒 Movie Session ViewSet
class MovieSessionViewSet(viewsets.ModelViewSet):

    queryset = MovieSession.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    serializer_class = MovieSessionSerializer

    def get_queryset(self):
        qs = MovieSession.objects.select_related(
            "movie", "cinema_hall"
        ).annotate(
            tickets_available=F("cinema_hall__rows")
            * F("cinema_hall__seats_in_row")
            - Count("tickets")
        )
        date_str = self.request.query_params.get("date")
        movie_id = self.request.query_params.get("movie")

        if date_str:
            parsed_date = parse_date(date_str)
            if parsed_date:
                qs = qs.filter(show_time__date=parsed_date)
        if movie_id and movie_id.isdigit():
            qs = qs.filter(movie_id=int(movie_id))

        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSessionListSerializer
        if self.action == "retrieve":
            return MovieSessionDetailSerializer
        return MovieSessionSerializer


# 🎟️ Order ViewSet
class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):

    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = OrderPagination

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "tickets__movie_session__movie",
            "tickets__movie_session__cinema_hall",
        )

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
