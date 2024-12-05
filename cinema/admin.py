from django.contrib import admin

from cinema.models import (
    Actor,
    CinemaHall,
    Genre,
    Movie,
    MovieSession,
    Order,
    Ticket,
)


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ["name", "rows", "seats_in_row"]
    search_fields = ["name"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
    search_fields = ["first_name", "last_name"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "duration"]
    search_fields = ["title"]
    filter_horizontal = ["actors", "genres"]


@admin.register(MovieSession)
class MovieSessionAdmin(admin.ModelAdmin):
    list_display = ["movie", "cinema_hall", "show_time"]
    list_filter = ["show_time", "movie", "cinema_hall"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["created_at", "user"]
    list_filter = ["created_at"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["movie_session", "order", "row", "seat"]
    list_filter = ["movie_session"]
