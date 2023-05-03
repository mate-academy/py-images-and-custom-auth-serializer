import os
import uuid

from django.utils.text import slugify


def movie_image_file_path(movie, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(movie.title)}-{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/movies/", filename)
