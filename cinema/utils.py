import os.path
from uuid import uuid4

from django.utils.text import slugify


def generate_movie_path(movie, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(movie.title)}-{uuid4()}{extension}"
    return os.path.join("uploads/movies/", filename)
