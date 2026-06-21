from django.contrib import admin

from .models import (
    CinemaHall,
    Genre,
    Actor,
    Movie,
    MovieSession,
    Order,
    Ticket,
)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "duration")
    search_fields = ("title",)


admin.site.register(CinemaHall)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(MovieSession)
admin.site.register(Order)
admin.site.register(Ticket)
