import os
import uuid

from django.db import models
from django.utils.text import slugify


def movie_image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "movies", filename)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to=movie_image_file_path,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title
