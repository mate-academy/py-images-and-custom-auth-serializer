from rest_framework import serializers
from cinema.models import (
    Genre,
    Actor,
    CinemaHall,
    Movie,
    MovieSession,
    Order,
    Ticket,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class MovieSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = Movie
        fields = ("id", "title", "description", "duration", "genres", "actors", "image")


class MovieListSerializer(MovieSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta(MovieSerializer.Meta):
        fields = ("id", "title", "duration", "image")


class MovieDetailSerializer(MovieSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    image = serializers.ImageField(read_only=True)

    class Meta(MovieSerializer.Meta):
        fields = ("id", "title", "description", "duration", "genres", "actors", "image")


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall")


class MovieSessionListSerializer(serializers.ModelSerializer):
    movie_image = serializers.SerializerMethodField()
    movie = serializers.CharField(source="movie.title")
    cinema_hall = serializers.CharField(source="cinema_hall.name")

    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall", "tickets_available", "movie_image")

    def get_movie_image(self, obj):
        if obj.movie.image:
            return self.context['request'].build_absolute_uri(obj.movie.image.url)
        return None


class MovieSessionDetailSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    cinema_hall = CinemaHallSerializer(read_only=True)

    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall", "tickets_available")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")


class OrderListSerializer(OrderSerializer):
    tickets = serializers.StringRelatedField(many=True, read_only=True)

    class Meta(OrderSerializer.Meta):
        fields = ("id", "tickets", "created_at")