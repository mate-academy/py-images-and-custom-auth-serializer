from rest_framework import viewsets
from cinema.models import Genre, Actor, CinemaHall, Movie, MovieSession, Order
from cinema.serializers import (
    GenreSerializer, ActorSerializer, CinemaHallSerializer,
    MovieSerializer, MovieListSerializer,
    MovieSessionSerializer, MovieSessionListSerializer,
    OrderSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MovieListSerializer
        return MovieSerializer


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MovieSessionListSerializer
        return MovieSessionSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("tickets__movie_session__movie")
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Garante que o usuário só veja seus próprios pedidos
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Atribui o usuário logado ao pedido
        serializer.save(user=self.request.user)
