from rest_framework import serializers
from django.db import transaction
from django.core.exceptions import ValidationError

from cinema.models import (
    Genre,
    Actor,
    CinemaHall,
    Movie,
    MovieSession,
    Ticket,
    Order,
)


# 🎬 Movie Image Upload
class MovieImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("image",)
        extra_kwargs = {"image": {"required": True}}


# 📚 Basic Entities
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


# 🎥 Movie Serializers
class MovieBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "title", "description", "duration", "genres", "actors")


class MovieListSerializer(MovieBaseSerializer):
    image = serializers.ImageField(read_only=True)
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )

    class Meta(MovieBaseSerializer.Meta):
        fields = MovieBaseSerializer.Meta.fields + ("image",)


class MovieDetailSerializer(MovieBaseSerializer):
    image = serializers.ImageField(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta(MovieBaseSerializer.Meta):
        fields = MovieBaseSerializer.Meta.fields + ("image",)


# Alias for MovieSerializer to resolve import errors
class MovieSerializer(MovieBaseSerializer):
    pass


# 🕒 Movie Session Serializers
class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall")


class MovieSessionListSerializer(serializers.ModelSerializer):
    movie_image = serializers.SerializerMethodField()
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    cinema_hall_name = serializers.CharField(
        source="cinema_hall.name", read_only=True
    )
    cinema_hall_capacity = serializers.IntegerField(
        source="cinema_hall.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = MovieSession
        fields = (
            "id",
            "show_time",
            "movie_title",
            "cinema_hall_name",
            "cinema_hall_capacity",
            "tickets_available",
            "movie_image",
        )

    def get_movie_image(self, obj):
        if obj.movie and obj.movie.image:
            request = self.context.get("request")
            image_url = obj.movie.image.url
            if request is not None:
                return request.build_absolute_uri(image_url)
            return image_url
        return None


class MovieSessionDetailSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    cinema_hall = CinemaHallSerializer(read_only=True)
    taken_places = serializers.SerializerMethodField()

    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall", "taken_places")

    def get_taken_places(self, obj):
        return TicketSeatsSerializer(obj.tickets.all(), many=True).data


# 🎟️ Ticket Serializers
class TicketBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "movie_session")


class TicketSerializer(TicketBaseSerializer):
    def validate(self, attrs):
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["movie_session"],
            ValidationError,
        )
        return super().validate(attrs)


class TicketListSerializer(TicketBaseSerializer):
    movie_session = MovieSessionListSerializer(read_only=True)


class TicketSeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


# 🧾 Order Serializers
class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            Ticket.objects.bulk_create(
                [
                    Ticket(order=order, **ticket_data)
                    for ticket_data in tickets_data
                ]
            )
        return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
