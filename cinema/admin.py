from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from .models import (
    CinemaHall,
    Genre,
    Actor,
    Movie,
    MovieSession,
    Order,
    Ticket,
)

TokenAdmin.raw_id_fields = ["user"]

admin.site.register(CinemaHall)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(MovieSession)
admin.site.register(Order)
admin.site.register(Ticket)
