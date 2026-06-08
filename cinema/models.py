import os
import uuid
from typing import Any

from django.db import models
from django.utils.text import slugify


def movie_image_file_path(instance: Any, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    movie_slug = slugify(instance.title)
    filename = f"{movie_slug}-{uuid.uuid4()}{extension}"
    return os.path.join(
        "uploads",
        "movies",
        filename
    )


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        ordering = ["first_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    image = models.ImageField(
        null=True,
        upload_to=movie_image_file_path,
        blank=True
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class MovieSession(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )
    cinema_hall = models.ForeignKey(
        CinemaHall,
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["-show_time"]

    def __str__(self) -> str:
        return f"{self.movie.title} {self.show_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        unique_together = ("movie_session", "row", "seat")
        ordering = ["row", "seat"]

    def __str__(self) -> str:
        return (f"{str(self.movie_session)} "
                f"(row: {self.row}, seat: {self.seat})")
