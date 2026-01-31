import os
import uuid

from django.db import models
from django.utils.text import slugify


def movie_image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "movies", filename)


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    image = models.ImageField(
        upload_to=movie_image_file_path,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(
        CinemaHall,
        on_delete=models.CASCADE,
        related_name="movie_sessions",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="movie_sessions",
    )

    def __str__(self):
        return f"{self.movie.title} {self.show_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="orders",
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"<Order: {self.created_at}>"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self):
        return (
            f"<Ticket: {self.movie_session} "
            f"(row: {self.row}, seat: {self.seat})>"
        )
