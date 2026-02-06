from django.contrib import admin
# Certifique-se de que todos esses nomes existem no seu models.py
from cinema.models import (
    Bus,
    Facility,
    Genre,
    Actor,
    Movie,
    CinemaHall,
    MovieSession,
    Order,
    Ticket
)

admin.site.register(Bus)
admin.site.register(Facility)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(CinemaHall)
admin.site.register(MovieSession)
admin.site.register(Order)
admin.site.register(Ticket)
